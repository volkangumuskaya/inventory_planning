import streamlit as st
from pages import inititate_planning_tool

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "",
    ["Home", "About", "Contact"]
)

# Show content based on the selected page
if page == "Home":
    inititate_planning_tool.show()
elif page == "About":
    st.title("About Page")
    st.write("This is the about page.")
elif page == "Contact":
    st.title("Contact Page")
    st.write("This is the contact page.")
