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
    ["Solve_model","Module_matching"]
)

# import os
# print("Main Current Working Directory:", os.getcwd())

# Show content based on the selected page
if page == "Solve_model":
    # test_page.show()
    inititate_planning_tool.show()
elif page == "About":
    st.title("About Page")
    st.write("This is the about page.")
elif page == "Module_matching":
    st.header("Module matching",divider=True)
    module_matching.show()
# elif page == "Contact":
#     test_page.show()

