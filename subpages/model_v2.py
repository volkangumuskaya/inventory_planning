# Import the PuLP library
import streamlit as st
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum,LpInteger,LpContinuous,LpBinary,LpStatus,value
import random
import numpy as np
from collections import defaultdict
import pickle
import os
import sys
from pathlib import Path

seed=random.randint(0,100)
random.seed(50)

sys.path.append(str(Path(__file__).parent))

from data_class_script_v2 import (Customer, Order, Product, Resource,
                                  generate_customers, generate_orders, generate_products, generate_resources,
                                  determine_total_quantity_per_product,print_orders,retrieve_fulfill_times)

import time
start=time.time()

def show():
    # Initialize session state for the button click
    if "show_solve_section" not in st.session_state:
        st.session_state.show_solve_section = False
    if "show_build_section" not in st.session_state:
        st.session_state.show_build_section = False
    if "show_output_section" not in st.session_state:
        st.session_state.show_output_section = False
    
    
    # Set the title that appears at the top of the page.
    st.image('images/el-chalten-min.jpg','El Chalten, Patagonia')
    st.header('A multi-horizon planning tool v2', divider=True)
    '''
    This is the second model to create and solve an inventory planning problem with time periods. Enter problem parameters and press 'Build' to generate a model. Upon doing so, you may download the model as txt file and 'Solve'.
    '''
        
    #Show measurements only for selected station
    st.header('Problem parameters', divider=True)
    # Create three columns with custom widths
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Number of time periods")
        n_time_period = st.selectbox('#Time periods',list(range(10,21)),index=0)
        time_ids=list(range(n_time_period))
        st.subheader("Resources")
        n_resource = st.selectbox('#Resources',list(range(2,3)),index=0)
        n_customer = st.selectbox('#Customer',list(range(3,4)),index=0)
    with col2:
        st.subheader("Orders")
        n_order = st.select_slider(
            "Select number of orders",
            options=list([500,1000,1500,2000]),
            value=1000,
        )
        min_q_per_order, max_q_per_order = st.select_slider(
            "Select min/max resources needed per product",
            options=[20,30,40,50,60,70,80,90,100],
            value=(50, 100),
        )

    min_criticality=4
    max_criticality=10

   # Create three columns with custom widths
    col1,col2,col3 = st.columns([1,1,1])
    with col1:
      if st.button("BUILD MODEL", type="primary"):
        try:
            random.seed(42)
            #Set of periods
            ##GENERATE MAIN COMPONENTS RANDOMLY
            time_ids=list(range(n_time_period))
            resources=generate_resources(n_resources=n_resource) #generate resource types
            products=generate_products()#using the special structure where
                                        # product0 -> resource0,
                                        # product1 -> resource1,
            #                           # product2 -> resource 0 or 1
            customers=generate_customers(n_customers=n_customer)
            
            orders=generate_orders(n_orders=n_order,products=products,customers=customers,time_periods=time_ids,
                                   min_product_type=1,max_product_type=1,
                                   min_product_amt=min_q_per_order,max_product_amt=max_q_per_order)

            total_quantity_per_product=determine_total_quantity_per_product(orders_f=orders,products_f=products)
            total_quantity_all_products=sum(total_quantity_per_product.values())
            
            # Decision variables and indices
            resource_ids=[x.resource_id for x in resources]
            product_ids=[x.product_id for x in products]
            order_ids=[x.order_id for x in orders]
            resource_names=[x.name for x in resources]
            product_names=[x.name for x in products]
            order_names=[f'order_{x.order_id}' for x in orders]
            
            criticality=[random.randint(a=min_criticality,b=max_criticality)/max_criticality for x in orders]
            capacities=[round(total_quantity_all_products/len(time_ids)/len(resources),0)+1 for x in resources]
                           
            ########
            # MODELING
            
            #BUILD MODEL
            #Decision vars
            # X: amount produced of resource R in time T
            x = LpVariable.dicts(name="production_p_r_t", indices=(product_ids,resource_ids,time_ids),lowBound= 0,upBound= None,cat=LpContinuous)
            # Y: 1 if order O is fulfilled in time T. We allow only complete fulfillment of orders/delivery
            y = LpVariable.dicts(name="order_fulfill_o_t", indices=(order_ids,time_ids),lowBound= 0,upBound= 1,cat=LpContinuous)
            # # 1 if order O is delayed in time T
            # order_delay = LpVariable.dicts(name="order_delay", indices=(order_ids,time_ids),lowBound= 0,upBound= None,cat=LpBinary)
            # starting inventory of resource R in time T
            inv = LpVariable.dicts(name="starting_inventory_p_t", indices=(product_ids,time_ids+[len(time_ids)]),
                                   lowBound= 0,upBound= None,cat=LpContinuous)
            
                
            # Create initial model
            prob = LpProblem("NXP_trial_v2", LpMinimize)
            
            # The objective function consists of resource and delay costs
            obj_func_production=[(t-o.deadline)**2*criticality[o.order_id]*y[o.order_id][t]*o.product[o.product_id] for o in orders for t in time_ids if t>o.deadline]
            prob += (lpSum(obj_func_production))
            
            #CONSTRAINTS
            #order fulfillment
            for o in orders:
                prob += (lpSum([y[o.order_id][t] for t in time_ids]) ==1,
                         f"Order_fulfill_order{o.order_id}")
                
            # Resource capacity constraints
            for t in time_ids:
                for r in resource_ids:
                    prob += (lpSum([p.resource_usage[r]*x[p.product_id][r][t] for p in products]) <= capacities[r],
                        f"Capacity_resource{r}_time{t}")
            
            # Starting inventory is 0
            for p in product_ids:
                prob += (inv[p][0] <= 0) , f"initial_starting_inventory_product{p}"
            
            # starting inventory + production  - resource needed to fulfill orders = ending inventory
            for t in time_ids:
                for p in product_ids:
                    prob += (
                        lpSum([x[p][r][t] for r in resource_ids])-
                        lpSum([o.product[p]*y[o.order_id][t] for o in orders])+
                        inv[p][t] == inv[p][t+1],
                        f"Inventory_balance_product{p}_time{t}",
                    )
            
            # The problem data is written to an .lp file
            prob.writeLP("nxp_v2.lp")
            
            # The problem is solved using PuLP's choice of Solver
            prob.solve()
            
            end=time.time()
            # Each variable printed
            
            
            total_delayed_units=0
            for o in orders:
                for t in time_ids:
                    check_sum=0
                    if (y[o.order_id][t].varValue>0.001)&(check_sum<=1.00):
                        check_sum+=o.deadline
                        if t>o.deadline:
                            total_delayed_units+=o.product[o.product_id]*y[o.order_id][t].varValue
                        # print(f'order:{o.order_id},deadline:{o.deadline},product:{o.product_id},var:{y[o.order_id][t]},q:{o.product[o.product_id]},val:{y[o.order_id][t].varValue}')
            
            print(f'Used seed:{seed}')
            # n variables
            print("# variables = ", len(prob.variables()))
            # The optimised objective function value is printed to the screen
            print("# constraints = ", len(prob.constraints))
            # The optimised objective function value is printed to the screen
            print("Total Cost = ", value(prob.objective))
            # number of delayed quantities
            print("Total delayed product quantity:", total_delayed_units)
            print("Total quantity:", total_quantity_all_products)
            print(f'% delayed items: %{round(total_delayed_units/total_quantity_all_products*100,2)}')
            # The status of the solution is printed to the screen
            print("Status:", LpStatus[prob.status])
            print("Time total:",end-start)
            
            #retrieve fulfillment times
            orders=retrieve_fulfill_times(orders_tmp=orders,y_vars=y,time_periods=time_ids)
            
            for p, r, t in ((p, r, t) for p in product_ids for r in resource_ids for t in time_ids):
                if x[p][r][t].varValue > 0:  # Check if the variable's value is non-zero
                    print(f"x[{p},{r},{t}]  | name: {x[p][r][t].name}: {x[p][r][t].varValue}")
            
            #Create df s
            order_df=pd.DataFrame([(obj.order_id,
                                    obj.customer_name,
                                    obj.deadline,
                                    obj.product_id,
                                    obj.product[obj.product_id],
                                    criticality[obj.order_id],
                                    obj.fulfilled) for obj in orders],
                                  columns=['Order_ID', 'Customer_Name', 'Deadline', 'Product_ID','Product_Amount','Criticality','Fulfilled_time'])
            order_df['Delay_status'] = np.where(order_df['Fulfilled_time']>order_df['Deadline'], 'Delayed', 'On_time')
            order_df['Delay_duration'] = np.where(order_df['Fulfilled_time']>order_df['Deadline'], order_df['Fulfilled_time']>order_df['Deadline'], 0)

            st.success(f"Total Cost = {value(prob.objective)}")
                
        except:
          st.write('hllo')
