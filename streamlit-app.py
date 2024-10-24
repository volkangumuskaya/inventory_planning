
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
