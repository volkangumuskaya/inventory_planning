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
    
  
