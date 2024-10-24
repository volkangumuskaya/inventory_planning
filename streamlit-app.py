import streamlit as st

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='volkan-ai',
    layout="wide",
    page_icon=':rainbow:', # This is an emoji shortcode. Could be a URL too.
    # page_icon="images/weather_icon.png"
)

st.sidebar.header("About",divider='orange')
with st.sidebar:
    st.image('images/profile_round.png',width=200,caption="https://www.linkedin.com/in/volkangumuskaya/")
    
'''
# Example app
'''

#Show measurements only for selected station
st.header('Problem parameters', divider=True)

n_resources = st.selectbox(
    'Select station for latest measurements',
    [1,2,3])

from_year, to_year = st.select_slider(
        "Select a range of date",
        options=range(5),
        value=(2, 4),
    )
