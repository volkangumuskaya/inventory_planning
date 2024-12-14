from time import sleep
import streamlit as st

def initiate_plan():
    option = st.selectbox(
        "How are ya",
        ("Select contact method...", "ok", "not so much", "bad"),
        )
    if option != "Select contact method...":
        # Logic to execute when a valid order is selected
        message_tmp = {"role": "assistant", "content": f"User told us she is {option}"}
        st.session_state.messages.append(message_tmp)
        avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
        with st.chat_message(message_tmp["role"], avatar=avatar):
            st.markdown(message_tmp["content"])

def modify_plan():
    option = st.selectbox(
        "How would you like to be contacted?",
        ("Select contact method...", "Email", "Home phone", "Mobile phone"),
        )
    if option != "Select contact method...":
        # Logic to execute when a valid order is selected
        message_tmp = {"role": "assistant", "content": f"User has selected:{option}"}
        avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
        with st.chat_message(message_tmp["role"], avatar=avatar):
            st.markdown(message_tmp["content"])


def show_bot():

    st.write(
        f"""This is an application to match user text with predefined modules. You may select from the list or just write as free text. \n""")

    # Initialize chat history and system prompt
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Start with an empty chat history
        # st.session_state.welcome_message_shown = False
    if 'chatbot_active' not in st.session_state:
        st.session_state.chatbot_active = True
    if 'selected_module' not in st.session_state:
        st.session_state.selected_module = None

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if st.session_state.chatbot_active:
        if prompt := st.chat_input("Enter your prompt here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.selected_module=prompt
            with st.chat_message("user", avatar='👨‍💻'):
                st.markdown(prompt)

    if st.session_state.selected_module=='0':
        initiate_plan()
    if st.session_state.selected_module=='1':
        modify_plan()
        # option = st.selectbox(
        #     "How would you like to be contacted?",
        #     ("Select contact method...", "Email", "Home phone", "Mobile phone"),
        #     )
        # if option != "Select contact method...":
        #     # Logic to execute when a valid order is selected
        #     message_tmp = {"role": "user", "content": f"User has selected:{option}"}
        #     st.session_state.messages.append(message_tmp)
        #     with st.chat_message("user", avatar='👨‍💻'):
        #         st.markdown(message_tmp["content"])

if __name__ == '__main__':
    show_bot()