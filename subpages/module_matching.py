
import streamlit as st


from typing import Generator  # Used to display chatbot
from groq import Groq  # used to make API calls to llama
import requests  # used to make API call

import re
from pulp import value

from subpages.classes_and_generating_functions import retrieve_fulfill_times
from subpages.model_functions import create_model,add_objective_terms_v2, check_delayed_orders

# WARNING!
GROQ_API_KEY = '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'

# LLM model used and max_tokens
model_option = 'llama3-70b-8192'
max_tokens = 1024

def initiate_create_plan():

   # Creating the original model
    prob_tmp, x_tmp, y_tmp, inv_tmp = create_model(
        resources=st.session_state.resources, products=st.session_state.products,
        customers=st.session_state.customers, orders=st.session_state.orders,
        time_ids=st.session_state.time_ids, min_criticality=st.session_state.min_criticality,
        max_criticality=st.session_state.max_criticality, seed=st.session_state.seed)

    prob_tmp.solve()

   # Updating orders object based on the solution. Below are the specific attributes assigned
   # fullfilled : the time an order is completely fulfilled
   # delay_status: 'on_time' or 'delayed'
   # delay_duration: number of time periods delayed
    orders_tmp = retrieve_fulfill_times(
        orders_tmp=st.session_state.orders,
        y_vars=y_tmp,
        time_periods=st.session_state.time_ids)
    # Create a list of order id's to be displayed in chat for user reference
    delayed_orders_tmp, total_delayed_units_tmp = check_delayed_orders(
        f_orders=orders_tmp, f_y=y_tmp, f_time_ids=st.session_state.time_ids)


    # Solve original model
    prob_tmp.solve()
    # Append a brief message to be displayed in chatbot about solution
    st.session_state.messages.append({"role": "assistant", "content": f"**Delayed orders:** {delayed_orders_tmp}  \n"
                                                                      f"**Total # of delayed products :** {round(total_delayed_units_tmp, 0)}  \n"
                                                                      f"**Objective function:** {round(value(prob_tmp.objective), 1)}"})

    # Immediately display the message
    avatar = '🤖'
    with st.chat_message("assistant", avatar=avatar):
        st.markdown(f"**Delayed orders:** {delayed_orders_tmp}")
        st.markdown(f"**Total # of delayed products :** {round(total_delayed_units_tmp, 0)}")
        st.markdown(f"**Objective function value:** {round(value(prob_tmp.objective), 1)}")

def modify_plan():
    """
    Placeholder for future
    """
    st.write('Modify plan invoked successfully')


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def get_insights():
    """
    Placeholder for a module that will provide more detailed information
    """
    st.write('get_insights invoked successfully')

def download_all_results_production_schedule():
    """
    Placeholder for a module that will allow user to download all the solution
    """
    st.write('download_all_results_production_schedule invoked successfully')


def prioritize_orders():
    """
    Module that will
    1) Display the delayed orders so that user can choose one of the delayed orders
    2) Get a list of orders to be prioritized using selectbox
    3) Create a new model with an increased penalty for the prioritized order
    4) Solve the new model and summarize new solution
    """

    # When we create wisgets such as buttons, selectboxes etc in streamlit, we may need an id of the widget
    # This variable below, i.e. st.session_state.counter helps to keep track of which select box to be displayed and which not
    # Please check https://docs.streamlit.io/develop/concepts/architecture/widget-behavior for more explanation
    if 'counter' not in st.session_state:
        st.session_state.counter=0

    # Create original model and solve
    st.write(f'Prioritize order module invoked')
    prob_tmp, x_tmp, y_tmp, inv_tmp = create_model(
        resources=st.session_state.resources, products=st.session_state.products,
        customers=st.session_state.customers, orders=st.session_state.orders,
        time_ids=st.session_state.time_ids, min_criticality=st.session_state.min_criticality,
        max_criticality=st.session_state.max_criticality, seed=st.session_state.seed)

    prob_tmp.solve()
    # Updating orders object based on the solution. Below are the specific attributes assigned
    # fullfilled : the time an order is completely fulfilled
    # delay_status: 'on_time' or 'delayed'
    # delay_duration: number of time periods delayed
    orders_tmp = retrieve_fulfill_times(
        orders_tmp=st.session_state.orders,
        y_vars=y_tmp,
        time_periods=st.session_state.time_ids)
    # Create a list of order id's to be displayed in chat for user reference
    delayed_orders_tmp, total_delayed_units_tmp = check_delayed_orders(
        f_orders=orders_tmp, f_y=y_tmp, f_time_ids=st.session_state.time_ids)

    # Append a message to chatbot to be displayed
    message_tmp = {"role": "assistant", "content": f"Original Total Cost = {round(value(prob_tmp.objective), 1)}  \n"
                                                   f"Original # delayed units = {round(total_delayed_units_tmp, 0)}  \n"
                                                   f"Original Delayed orders = {delayed_orders_tmp}"}
    avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message_tmp["role"], avatar=avatar):
        st.markdown(message_tmp["content"])

    # Below is the part corresponding to creating the selectbox for getting order id's from user to be prioritized
    # Create the list of orders to be displayed in the selectbox widget
    placeholder_text = "Select order id..."
    all_options = [i for i in range(0, len(st.session_state.orders))]
    all_options.insert(0, placeholder_text)

    # Create a placeholder message for the selectbox
    multiselect_placeholder = st.empty()

    # Render the selectbox with the default index set to 0
    selected_options = multiselect_placeholder.multiselect(
        label=placeholder_text,
        options=all_options,
        key=st.session_state.counter  # Unique key for this multiselect box
        )


    # Check if the user has selected any orders, if so proceed. Otherwise take no action
    if len(selected_options) > 1 and selected_options[0] == placeholder_text:
        # If the user selects the placeholder text, we treat it as no valid selection
        st.warning("Please select at least one order to prioritize.")
    if st.button("Prioritize Selected Orders"):
        if selected_options != [0]:
            st.session_state.counter += 1

            # Display a message when a valid order is selected by user
            message_tmp = {"role": "assistant", "content": f"User has selected the order(s): {selected_options}"}
            avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
            with st.chat_message(message_tmp["role"], avatar=avatar):
                st.markdown(message_tmp["content"])
            st.session_state.messages.append(message_tmp)

            # Below we add new terms to the objective function of the original model, i.e. prob_tmp
            # New terms are only added for the orders to be priortized, i.e. selected_options
            # This new model will then be solved
            prob_tmp = add_objective_terms_v2(
                model=prob_tmp,
                order_list=[st.session_state.orders[i] for i in selected_options if i != 0],
                multiplier=9, criticality=st.session_state.criticality,
                y_f=y_tmp,
                time_ids_f=st.session_state.time_ids)
            prob_tmp.solve()
            orders_tmp = retrieve_fulfill_times(
                orders_tmp=st.session_state.orders,
                y_vars=y_tmp,
                time_periods=st.session_state.time_ids)
            delayed_orders_tmp, total_delayed_units_tmp = check_delayed_orders(
                f_orders=orders_tmp, f_y=y_tmp, f_time_ids=st.session_state.time_ids)

            # Add a message to chatbot to be displayed
            message_tmp = {"role": "assistant",
                           "content": f"New Total Cost after prioritize = {round(value(prob_tmp.objective), 1)}  \n"
                                      f"New # delayed units = {round(total_delayed_units_tmp,0)}  \n"
                                      f"New Delayed orders after prioritize = {delayed_orders_tmp}"}

            # Immediately display this message
            avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
            with st.chat_message(message_tmp["role"], avatar=avatar):
                st.markdown(message_tmp["content"])
            st.session_state.messages.append(message_tmp)

            # Clear the selectbox after a selection is made
            multiselect_placeholder.empty()

def list_orders_of_a_customer():
    """
        Placeholder for a module that will list all orders from a customer
    """
    st.write('list_orders_of_a_customer invoked successfully')

def change_production_capacity_of_a_machin_resource():
    """
            Placeholder for a module that will modify capacities
    """
    st.write('change_production_capacity_of_a_machin_resource invoked successfully')

# List of models as text. This list will be passed to LLM so that it can match user prompt with a module
module_name_list = ['Initiate/create a plan',
                    'Modify the plan',
                    'Get insights',
                    'Download all results / production schedule',
                    'Prioritize orders',
                    'List orders of a customer',
                    'Change production capacity of a machine/resource '
                    ]

def extract_module_from_response(response: str):
    # Regex to capture the module name from LLM s response in the format: "The module match is: "
    match = re.search(r"The module match is: (.+)", response)
    if match:
        return match.group(1)  # Return the module name
    return None  # If no match found


def show():
    """
    This is the main function invoked when user selects module_matching from the sidebar.
    """
    nl = '  \n'
    module_names = f"{nl}{nl.join(module_name_list)}"

    # System prompt fed to LLM (not displayed to the user)
    SYSTEM_PROMPT = f'''You are a specific AI assistant that try to understand what user wants and will invoke a number of modules. 
    If you find a reasonable match, I want you to respond in the format: The module match is: [Module name]
    If you cannot find a reasonable match, ask the user to try again by saying: I could not find a reasonable match, please try again or select from the list.
    You cannot respond with anything else. This is a strict requirement.
    The module names are as follows: \n
    {module_names} 
    '''

    # Add header and some explanations to the page
    st.header('Interaction modules', divider=True)
    st.markdown(
        '''
        Here, the user can interact with the model by typing queries.    
        The list of modules are on the sidebar.  
        Currently, **'Initiate/create a plan'** and **'Prioritize orders'** modules are active. 
        '''
        )

    # initiate API
    client = Groq(
        # api_key=st.secrets["GROQ_API_KEY"] # Normally this is the way to use API key
        api_key=GROQ_API_KEY
        )

    # Initialize some session state parameters
    if 'chatbot_active' not in st.session_state:
        st.session_state.chatbot_active = True
    if 'selected_module' not in st.session_state:
        st.session_state.selected_module = None

    st.session_state.selected_order=None


    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # This part corresponds to gettig user input and making LLM call.
    # 1) User writes something via the chat_input widget
    # 2) LLM API is invoked. Here LLM only aims to match user text with list of modules
    # 3) Based on response, selected_module variable is updated
    # 4) A module is invoked based on selected_module

    if st.session_state.chatbot_active:
        # 1) Get user input
        if prompt := st.chat_input("Enter your prompt here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            # User input is displayed in chat
            st.session_state.selected_module = prompt
            with st.chat_message("user", avatar='👨‍💻'):
                st.markdown(prompt)

            # 2) LLM is invoked and response fethced from Groq API. The response is chat_completion
            try:
                chat_completion = client.chat.completions.create(
                    model=model_option,
                    messages=[
                                 {"role": "system", "content": SYSTEM_PROMPT}
                                 ] + st.session_state.messages,  # Add system prompt to API context
                    max_tokens=max_tokens,
                    stream=True
                    )

                # Use the generator function with st.write_stream to create the full_response text
                with st.chat_message("assistant", avatar="🤖"):
                    chat_responses_generator = generate_chat_responses(chat_completion)
                    full_response = st.write_stream(chat_responses_generator)
            except Exception as e:
                st.error(e, icon="🚨")

            # Append the full_response to session_state.messages
            if isinstance(full_response, str):
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response})
            else:
                # Handle the case where full_response is not a string
                combined_response = "\n".join(str(item) for item in full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": combined_response})

            # 3) Based on response, selected_module is determined
            st.session_state.selected_module=extract_module_from_response(full_response)

    # 4) Corresponding module is invoked if exists
    if st.session_state.selected_module == "Initiate/create a plan":
        initiate_create_plan()
    if st.session_state.selected_module == 'Modify the plan':
        modify_plan()
    if st.session_state.selected_module == 'Prioritize orders':
        prioritize_orders()
    else:
        st.session_state.messages.append({"role": "assistant", "content": "This module is not in effect as of now."})



