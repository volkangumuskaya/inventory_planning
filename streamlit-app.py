import streamlit as st
from subpages import inititate_planning_tool,test_page,module_matching
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
    ["Model v0",'Model v1',"Module matching"]
)

# import os
# print("Main Current Working Directory:", os.getcwd())

# Show content based on the selected page
if page == "Model v0":
    # test_page.show()
    inititate_planning_tool.show()
elif page == "Model v1":
    st.header("Model v1",divider=True)
    st.write("This is the about page.")
elif page == "Module matching":
    st.header("Module matching",divider=True)
    module_matching.show()
# elif page == "Contact":
#     test_page.show()

