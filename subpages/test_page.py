import streamlit as st
# Import the PuLP library
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum,LpInteger,LpContinuous,LpBinary,LpStatus,value
import random
from collections import defaultdict
import pickle
import os
import sys
from pathlib import Path

st.write("hi first")
st.write("here is first version:",pd.__version__)

Add the root directory to sys.path
sys.path.append(str(Path(__file__).parent))
from data_class_script import Customer, Order, Product, Resource, generate_customers, generate_orders, generate_products, generate_resources

def show():
    # import pandas as pd
    st.write("here is version:",pd.__version__)
    unit_delay_cost=10000
    # Initialize session state for the button click
    if "show_solve_section" not in st.session_state:
        st.session_state.show_solve_section = False
    if "show_build_section" not in st.session_state:
        st.session_state.show_build_section = False
    if "show_output_section" not in st.session_state:
        st.session_state.show_output_section = False

     # Set the title that appears at the top of the page.
    st.image('images/el-chalten-min.jpg','El Chalten, Patagonia')
    st.header('A multi-horizon planning tool ', divider=True)
    '''
    This is an example tool to create and solve an inventory planning problem with time periods. Enter problem parameters and press 'Build' to generate a model. Upon doing so, you may download the model as txt file and 'Solve'.
    '''
    # st.sidebar.header("About",divider='orange')
    # with st.sidebar:
    #     st.image('images/profile_round.png',width=200,caption="https://www.linkedin.com/in/volkangumuskaya/")
        
    #Show measurements only for selected station
    st.header('Problem parameters', divider=True)
    # Create three columns with custom widths
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.subheader("Number of time periods")
        n_time_periods = st.selectbox('#Time periods',list(range(1,4)),index=1)
        time_ids=list(range(n_time_periods))
        st.subheader("Resources")
        n_resources = st.selectbox('#Resources',list(range(1,4)),index=1)
    
    with col2:
        st.subheader("Products")
        n_products = st.selectbox('#Products',list(range(5,11)),index=4)
        min_resource_needed, max_resource_needed = st.select_slider(
            "Select min/max resources needed per product",
            options=list(range(21)),
            value=(0, 20),
        )
    with col3:
        st.subheader("Orders")
        n_orders = st.selectbox('#Orders',list(range(1,31)),index=29)
        min_product_type, max_product_type = st.select_slider(
            "Select min/max product type per order",
            options=list(range(1,5)),
            value=(2, 4),
        )
        min_product_amt, max_product_amt = st.select_slider(
            "Select min/max #product per product type",
            options=list(range(21)),
            value=(10, 20),
        )
    
    # Create three columns with custom widths
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("BUILD MODEL", type="primary"):
            # import pandas as pd
            random.seed(42)
            #Set of periods
            
            unit_delay_cost=unit_delay_cost

            ##GENERATE MAIN COMPONENTS RANDOMLY
            resources=generate_resources(n_resources=n_resources) #generate resource types
            #generate products randomly. Each product requires random type of resources (one or multiple) and random amounts from 0-20
            products=generate_products(n_products=n_products,resources=resources, min_resource_needed=min_resource_needed, max_resource_needed=max_resource_needed)
            customers=generate_customers(n_customers=3)
            #generate orders randomly. One order consists of 2-4 types of products and 10-20 units for each
            orders=generate_orders(n_orders=n_orders,products=products,customers=customers,time_periods=time_ids,
                                min_product_type=min_product_type,max_product_type=max_product_type,
                                min_product_amt=min_product_amt,max_product_amt=max_product_amt)
            #Create dfs
            st.session_state.resource_df=pd.DataFrame([obj.__dict__ for obj in resources])
            st.session_state.product_df=pd.DataFrame([obj.__dict__ for obj in products])
            st.session_state.order_df=pd.DataFrame([(obj.order_id,obj.customer_name,obj.deadline,obj.product,obj.total_resource_usage) for obj in orders])
            st.session_state.order_df.columns=['OrderId','CustomerName','Deadline','ProductType-amount','ResourceType-amount']
            st.session_state.time_df=pd.DataFrame({'Time periods':time_ids})  
            
            #Calculate total resource for all orders in order to set capacities that will force some delays/avoid trivial solutions
            total_resource_needed=defaultdict(int)
            for o in orders:
                for r_id,r in enumerate(resources):
                    total_resource_needed[r_id]+=o.total_resource_usage[r_id]

            # Decision variables and indices
            resource_ids=[x.resource_id for x in resources]
            order_ids=[x.order_id for x in orders]

            delay_costs=[unit_delay_cost for x in orders]

            resource_names=[x.name for x in resources]
            product_names=[x.name for x in products]
            order_names=[f'order_{x.order_id}' for x in orders]

            resource_costs=[random.randint(a=2,b=8)/10 for _ in resources]
            resource_capacities=[round(total_resource_needed[r]*0.85/len(time_ids),0) for r in resource_ids]

            #BUILD MODEL
            #Decision vars
            # X: amount produced of resource R in time T
            x = LpVariable.dicts(name="resource_production", indices=(resource_ids,time_ids),lowBound= 0,upBound= None,cat=LpContinuous)
            # Y: 1 if order O is fulfilled in time T. We allow only complete fulfillment of orders/delivery
            y = LpVariable.dicts(name="order_fulfillment", indices=(order_ids,time_ids),lowBound= 0,upBound= None,cat=LpBinary)
            # 1 if order O is delayed in time T
            order_delay = LpVariable.dicts(name="order_delay", indices=(order_ids,time_ids),lowBound= 0,upBound= None,cat=LpBinary)
            # starting inventory of resource R in time T
            inv = LpVariable.dicts(name="starting_inventory", indices=(resource_ids,time_ids+[len(time_ids)]),
                                lowBound= 0,upBound= None,cat=LpContinuous)

            # Create initial model
            prob = LpProblem("NXP_trial", LpMinimize)

            # The objective function consists of resource and delay costs
            obj_func_production=[x[r][t]*resource_costs[r] for t in time_ids for r in resource_ids ]
            obj_func_delay_cost=[(order_delay[o][t])*delay_costs[o] for t in time_ids for o in order_ids if t>=orders[o].deadline]

            prob += (
                lpSum(obj_func_production+obj_func_delay_cost)
            )

            #CONSTRAINTS
            # Resource capacity constraints
            for t in time_ids:
                for r in resource_ids:
                    prob += (x[r][t] <= resource_capacities[r],f'Resource_cap_{resource_names[r]}_time_{t}')

            # Starting inventory is 0
            for r in resource_ids:
                prob += (inv[r][0] <= 0)

            # starting inventory + production  - resource needed to fulfill orders = ending inventory
            for t in time_ids:
                for r in resource_ids:
                    prob += (
                        lpSum([orders[o].total_resource_usage[r]*y[o][t] for o in order_ids])-x[r][t]-inv[r][t] == -inv[r][t+1],
                        f"Order_fulfill_{r}_{t}",
                    )

            #Delay=1 if order not fulfilled at deadline T or the following periods
            for o in order_ids:
                for t in time_ids:
                    if t>=orders[o].deadline:
                        prob += (
                            lpSum([y[o][t_s] for t_s in time_ids if t_s<=t]) + order_delay[o][t] >= 1,
                            f"Order_{o}_delay_in_{t}",
                            )
            # The problem data is written to an .lp file
            prob.writeLP("nxp.lp")
            st.success(f"Model built with: {n_resources} Resources, {n_products} Products, {n_orders} Orders!")

            with open('problem.pickle', 'wb') as handle:
                pickle.dump([prob,resource_names,product_names,order_names], handle, protocol=pickle.HIGHEST_PROTOCOL)
            
            st.session_state.show_build_section = True
            st.session_state.show_solve_section = True
            st.session_state.show_output_section = False
            st.session_state.problem=prob

