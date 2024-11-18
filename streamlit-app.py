import streamlit as st
from subpages import inititate_planning_tool
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

# import os
# print("Main Current Working Directory:", os.getcwd())




# Show content based on the selected page
if page == "Home":
    inititate_planning_tool.show()
elif page == "About":
    st.title("About Page")
    st.write("This is the about page.")
elif page == "Contact":
    st.title("Contact Page")
    st.write("This is the contact page.")
