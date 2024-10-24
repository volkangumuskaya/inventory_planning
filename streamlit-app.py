import streamlit as st
# Import the PuLP library
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum,LpInteger,LpContinuous,LpBinary,LpStatus,value
import random
from collections import defaultdict


from data_class_script import Customer, Order, Product, Resource, generate_customers, generate_orders, generate_products, generate_resources


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='volkan-ai',
    layout="wide",
    page_icon=':gear:', # This is an emoji shortcode. Could be a URL too.
    # page_icon="images/weather_icon.png"
)

# st.sidebar.header("About",divider='orange')
# with st.sidebar:
#     st.image('images/profile_round.png',width=200,caption="https://www.linkedin.com/in/volkangumuskaya/")
    
#Show measurements only for selected station
st.header('Problem parameters', divider=True)
# Create three columns with custom widths
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.header("Resources")
    n_resources = st.selectbox('#Resources',list(range(1,3)))

with col2:
    st.header("Products")
    n_products = st.selectbox('#Products',list(range(1,6)))
    min_resource_needed, max_resource_needed = st.select_slider(
        "Select min/max resources needed per product",
        options=list(range(21)),
        value=(0, 20),
    )
with col3:
    st.header("Orders")
    n_orders = st.selectbox('#Orders',list(range(1,31)))
    min_product_type, max_product_type = st.select_slider(
        "Select min/max product type per order",
        options=list(range(max(11,n_products))),
        value=(1, 2),
    )
    min_product_amt, max_product_amt = st.select_slider(
        "Select min/max #product per product type",
        options=list(range(21)),
        value=(10, 20),
    )

# Create three columns with custom widths
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("BUILD MODEL", type="primary"):
        try:
            random.seed(42)
            #Set of periods
            time_ids=[0,1,2]
            unit_delay_cost=10000

            

            ##GENERATE MAIN COMPONENTS RANDOMLY
            resources=generate_resources(n_resources=n_resources) #generate resource types
            #generate products randomly. Each product requires random type of resources (one or multiple) and random amounts from 0-20
            products=generate_products(n_products=n_products,resources=resources, min_resource_needed=min_resource_needed, max_resource_needed=max_resource_needed)
            customers=generate_customers(n_customers=3)
            #generate orders randomly. One order consists of 2-4 types of products and 10-20 units for each
            orders=generate_orders(n_orders=n_orders,products=products,customers=customers,time_periods=time_ids,
                                min_product_type=min_product_type,max_product_type=max_product_type,
                                min_product_amt=min_product_amt,max_product_amt=max_product_amt)

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
            st.write(f"Model built with: {n_resources} Resources, {n_products} Products, {n_orders} Orders!")
        except:
            st.write(f"Oops:/")


# Replace with your GitHub raw file URL
github_file_url = "https://github.com/volkangumuskaya/inventory_planning/blob/main/nxp.lp"
file_name = "Download model"
# Create a link with an icon
icon = ":file_download:"  # Icon for download
link = f'<a href="{github_file_url}" download="{file_name}">{icon} {file_name}</a>'

# Display the link
st.markdown(link, unsafe_allow_html=True)
