import streamlit as st

# Define pages as separate functions
def page_home():
    st.title("Home Page")
    st.write("Welcome to the home page!")

def page_about():
    st.title("About Page")
    st.write("This is the about page.")

def page_contact():
    st.title("Contact Page")
    st.write("Contact us here!")

# Add navigation to the sidebar
page = st.sidebar.selectbox("Navigation", ["Home", "About", "Contact"])

# Show selected page content
if page == "Home":
    page_home()
elif page == "About":
    page_about()
elif page == "Contact":
    page_contact()
