import streamlit as st

def modify_plan():
    # Initialize chat history and system prompt
    if "messages" not in st.session_state:
        st.session_state.messages = []  # Start with an empty chat history
        st.session_state.welcome_message_shown = False

    for message in st.session_state.messages:
        avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    st.write("Modify_plan invoked successfully")

    # Example list of orders
    orders_to_modify = [f"Order {i}" for i in range(1, 1001)]

    # Set a default placeholder for the selectbox
    placeholder_order = "Please select an order"

    # Add the placeholder to the list of options
    orders_to_modify_with_placeholder = [placeholder_order] + orders_to_modify

    # Display the selectbox
    selected_order = st.selectbox(
        "Select an order:",
        orders_to_modify_with_placeholder,
        key="order_selection"
        )

    # Check if the user has selected an order
    if selected_order != placeholder_order:
        # Logic to execute when a valid order is selected
        st.write(f"You selected: {selected_order}")
        st.session_state.messages.append({"role": "assistant", "content": f"You selected: {selected_order}"})
    else:
        # Message when no valid selection is made
        st.write("Please select an order to proceed.")
    st.write(st.session_state.messages)
def show_test():
    modify_plan()