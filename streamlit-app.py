import streamlit as st
from subpages import inititate_planning_tool,module_matching,model_v2
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
    ["Model v1",'Model v2',"Module matching"]
)

# import os
# print("Main Current Working Directory:", os.getcwd())

# Show content based on the selected page
if page == "Model v1":
    # test_page.show()
    inititate_planning_tool.show()
elif page == "Model v2":
    st.header("Model v2",divider=True)
    model_v2.show()
elif page == "Module matching":
    st.header("Module matching",divider=True)
    module_matching.show()
# elif page == "Contact":
#     test_page.show()

