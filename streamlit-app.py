import streamlit as st

# Inject CSS for minor styling adjustments
st.markdown("""
    <style>
    .css-1aumxhk {
        font-size: 16px;
    }
    .stSidebar > div {
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation with direct clickable options
page = st.sidebar.radio("Navigation", ["Home", "About", "Contact"])

# Show content based on the selected page
if page == "Home":
    st.title("Home Page")
    st.write("Welcome to the home page!")

elif page == "About":
    st.title("About Page")
    st.write("This is the about page.")

elif page == "Contact":
    st.title("Contact Page")
    st.write("Contact us here!")
