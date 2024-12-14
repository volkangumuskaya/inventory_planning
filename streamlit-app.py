import streamlit as st
from streamlit import divider

# st.set_page_config(
#     page_title='volkan-ai',
#     layout="wide"
# )

from subpages import inititate_planning_tool
from subpages import module_matching
from subpages import model_v2
from subpages import default_model
import test
# Set the title and favicon that appear in the Browser's tab bar.
module_name_list = ['Initiate/create a plan',
                    'Modify the plan',
                    'Get insights',
                    'Download all results / production schedule',
                    'Prioritize orders',
                    # 'Prioritize all orders of a customer',
                    'List orders of a customer',
                    'Change production capacity of a machine/resource '
                    ]

# Sidebar navigation
# st.sidebar.title("Navigation",divider=True)
st.sidebar.header("**NAVIGATION**",divider=True)

page = st.sidebar.radio(
    "",
    # ["Model v1",'Model v2','Module v2.2',"Module matching",'test']
    ['Default model',"Module matching"]
)

# import os
# print("Main Current Working Directory:", os.getcwd())
# Initialize chat history and system prompt
if "messages" not in st.session_state:
  st.session_state.messages = []  # Start with an empty chat history
  st.session_state.welcome_message_shown = False

if page == "Model v2":
    st.header("Model v2",divider=True)
    model_v2.show()
elif page == "Default model":
    # st.header("Default model",divider=True)
    # st.sidebar.title("Module list")
    # module_selection = st.selectbox("Select a module from the list", module_name_list)

    default_model.show()
elif page == "Module matching":
    # st.sidebar.markdown("### Modules Available:")
    st.sidebar.header("Module list",divider=True)
    # st.sidebar.markdown("### Modules Available:")
    st.sidebar.text("\n".join(module_name_list))
    module_matching.show()
elif page=='test':
    st.header("Module matching", divider=True)
    test.show_test()
# elif page == "Contact":
#     test_page.show()

