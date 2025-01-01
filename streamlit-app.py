# This is the main script executed and served by streamlit servers.
# This app involves the following subscripts located in subpages folder.
# Detailed explanations are provided in the corresponding scripts. For reference to understand general structure:
#   streamlit-app.py                    : Main script executed to build the front end (i.e. streamlit page)
#   _init__.py                          : Executed under the ood to initialize session states
#   classes_and_generating_functions.py : Includes class structures and helper functions to generate the objects
#   default_model.py                    : Builds the default_model page where user can modify model parameters and solve
#   model_functions.py                  : Includes the helper functions related to building/modifying PuLp math model
#   module_matching                     : Builds module_matching page

import streamlit as st
st.set_page_config(
    page_title='volkan-ai',
    layout="wide"
)
import subpages
st.write('checkpoint1 streamlit-app.py')
from subpages import module_matching # Corresponds to the page where we have modules, e.g. initalize, priortize orders, etc
st.write('checkpoint2 streamlit-app.py')
from subpages import default_model # Corresponds to creating and solving a math model with customized parameters
st.write('checkpoint3 streamlit-app.py')
# Create sidebar
st.sidebar.header("**NAVIGATE**",divider=True) #This is the header. Note that **[text]** imposes bold format
# The list of modules to be displayed for reference only
module_name_list = ['Initiate/create a plan',
                    # 'Modify the plan',
                    'Get insights',
                    'Download all results / production schedule',
                    'Prioritize orders',
                    'List orders of a customer',
                    'Change production capacity of a machine/resource '
                    ]
# Radio button to switch between the pages.
page = st.sidebar.radio(
    "", # empty string can be replaced to add a small text
    ['Default model',"Module matching"]
    )

# Initialize chat history, this object stores all the messages to be displayed
# An avatar is displayed based on who writes the text, either the user or the assistant
if "messages" not in st.session_state:
    st.session_state.messages = []  # Start with an empty chat history
    st.session_state.welcome_message_shown = False
    # Below is nonfunctional but keeping it FYI. I use st.write for debugging just as I do when running python script
    # st.write("Messages Initialized")

# 'page' variable retrived from the radio button and used to activate the corresponding page
if page == "Default model":
    default_model.show()
elif page == "Module matching":
    st.sidebar.header("Module list",divider=True)
    st.sidebar.text("\n".join(module_name_list)) # The module list is diplayed for referenced
    module_matching.show()
