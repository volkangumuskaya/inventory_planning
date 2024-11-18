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
    
  
