import streamlit as st
# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='volkan-ai',
    layout="wide",
    # page_icon="images/weather_icon.png"
)
# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "",
    ["Home", "About", "Contact"]
)
# Import the PuLP library
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum,LpInteger,LpContinuous,LpBinary,LpStatus,value
import random
from collections import defaultdict
import pickle
import os
print("Main Current Working Directory:", os.getcwd())
st.write('hi again')
from subpages import inititate_planning_tool
st.write('hi again2')



# Show content based on the selected page
if page == "Home":
    st.write('hi again3')
    inititate_planning_tool.show()
    st.write('hi again4')
elif page == "About":
    st.title("About Page")
    st.write("This is the about page.")
elif page == "Contact":
    st.title("Contact Page")
    st.write("This is the contact page.")
