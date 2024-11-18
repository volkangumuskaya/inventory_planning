import streamlit as st
# Import the PuLP library
import pandas as pd
# from pulp import LpProblem, LpMinimize, LpVariable, lpSum,LpInteger,LpContinuous,LpBinary,LpStatus,value
# import random
# from collections import defaultdict
# import pickle
# import os
# import sys
# from pathlib import Path

st.write("hi first")
st.write("here is first version:",pd.__version__)

# Add the root directory to sys.path
# sys.path.append(str(Path(__file__).parent))
# from data_class_script import Customer, Order, Product, Resource, generate_customers, generate_orders, generate_products, generate_resources

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
            st.write('another version:',pd.__version__)
