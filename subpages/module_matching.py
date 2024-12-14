from time import sleep
import streamlit as st
from typing import Generator
from groq import Groq
import requests
import re
from pulp import LpProblem, LpMinimize, LpVariable, lpSum,LpInteger,LpContinuous,LpBinary,LpStatus,value
from requests import options
from prioritize_order import check_delayed_orders,add_objective_terms_v2
from subpages.data_class_script_v2 import (Customer, Order, Product, Resource,
                                  generate_customers, generate_orders, generate_products, generate_resources,
                                  determine_total_quantity_per_product,print_orders,retrieve_fulfill_times)
from subpages.model_functions import print_product_production,st_print_product_production

from subpages.model_functions import print_product_production,st_print_product_production
from subpages.model_functions import create_main_objects,create_obj_function,create_model
import time

def get_an_order():
    st.write('....Get_an_order invoked successfully')

    placeholder_text = "Select order id..."

    all_options = [i for i in range(0, len(st.session_state.orders))]
    all_options.insert(0, placeholder_text)

    # Create a placeholder for the selectbox
    selectbox_placeholder = st.empty()

    # Render the selectbox with the default index set to 0
    option = selectbox_placeholder.selectbox(
        label=placeholder_text,
        options=all_options,
        index=0,  # Default to the first option (placeholder_text)
        key="select_order"  # Unique key for this selectbox
    )

    st.write(f'option = {option}')
    st.write(f'all_options[0] = {all_options[0]}')
    st.write(f'st.session_state.selected_order = {st.session_state.selected_order}')

    # Check if the user has selected an order
    if (option != placeholder_text) and (st.session_state.selected_order is None):
        # Logic to execute when a valid order is selected
        message_tmp = {"role": "assistant", "content": f"User has selected the order: {option}"}
        avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
        with st.chat_message(message_tmp["role"], avatar=avatar):
            st.markdown(message_tmp["content"])
        st.session_state.messages.append(message_tmp)

        # Update session state
        st.session_state.selected_order = option
        message_tmp = {"role": "assistant",
                       "content": f"Session state order is now order {st.session_state.selected_order}"}
        avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
        with st.chat_message(message_tmp["role"], avatar=avatar):
            st.markdown(message_tmp["content"])

        # Clear the selectbox after a selection is made
        selectbox_placeholder.empty()
        st.write('Get an order ended')

def initiate_create_plan():
    # st.write('Initiate_create_plan invoked successfully')
    # st.session_state.messages.append({"role": "assistant", "content": f"Initiate_create_plan invoked"})
    prob_tmp, x_tmp, y_tmp, inv_tmp = create_model(
        resources=st.session_state.resources, products=st.session_state.products,
        customers=st.session_state.customers, orders=st.session_state.orders,
        time_ids=st.session_state.time_ids, min_criticality=st.session_state.min_criticality,
        max_criticality=st.session_state.max_criticality, seed=st.session_state.seed)
    prob_tmp.writeLP("before.lp")
    prob_tmp.solve()
    orders_tmp = retrieve_fulfill_times(
        orders_tmp=st.session_state.orders,
        y_vars=y_tmp,
        time_periods=st.session_state.time_ids)
    delayed_orders_tmp, total_delayed_units_tmp = check_delayed_orders(
        f_orders=orders_tmp, f_y=y_tmp, f_time_ids=st.session_state.time_ids)

    # current_prob=st.session_state.current_model
    # st.write("model loaded")
    prob_tmp.solve()
    # st.write("Model solved. Total Cost = ", round(value(current_prob.objective), 1))
    st.session_state.messages.append({"role": "assistant", "content": f"**Delayed orders:** {delayed_orders_tmp}  \n"
                                                                      f"**Total # of delayed products :** {round(total_delayed_units_tmp, 0)}  \n"
                                                                      f"**Objective function:** {round(value(prob_tmp.objective), 1)}"})

    avatar = '🤖'
    with st.chat_message("assistant", avatar=avatar):
        st.markdown(f"**Delayed orders:** {delayed_orders_tmp}")
        st.markdown(f"**Total # of delayed products :** {round(total_delayed_units_tmp, 0)}")

def modify_plan():
    # st.session_state.chatbot_active=False
    st.write('Modify plan invoked successfully')
    st.session_state.messages.append({"role": "assistant", "content": "Invalid or in-progress module."})
    # get_an_order()
    # if st.session_state.selected_order is not None:
    #     prioritize_an_order_v2(st.session_state.selected_order)
    #     st.write('Modify plan ended successfully')


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def get_insights():
    st.write('get_insights invoked successfully')

def download_all_results_production_schedule():
    st.write('download_all_results_production_schedule invoked successfully')


def prioritize_orders():
    if 'counter' not in st.session_state:
        st.session_state.counter=0
    st.write(f'Prioritize order module invoked')
    prob_tmp, x_tmp, y_tmp, inv_tmp = create_model(
        resources=st.session_state.resources, products=st.session_state.products,
        customers=st.session_state.customers, orders=st.session_state.orders,
        time_ids=st.session_state.time_ids, min_criticality=st.session_state.min_criticality,
        max_criticality=st.session_state.max_criticality, seed=st.session_state.seed)
    prob_tmp.writeLP("before.lp")
    prob_tmp.solve()
    orders_tmp = retrieve_fulfill_times(
        orders_tmp=st.session_state.orders,
        y_vars=y_tmp,
        time_periods=st.session_state.time_ids)
    delayed_orders_tmp, total_delayed_units_tmp = check_delayed_orders(
        f_orders=orders_tmp, f_y=y_tmp, f_time_ids=st.session_state.time_ids)
    # st_print_product_production(
    #     f_product_ids=st.session_state.product_ids, f_resource_ids=st.session_state.resource_ids,
    #     f_x=x_tmp, f_time_ids=st.session_state.time_ids)
    #
    # st.write("Original Total Cost = ", round(value(prob_tmp.objective), 1))
    # # number of delayed quantities
    # st.write("Original Total delayed product quantity = ", round(total_delayed_units_tmp, 2))
    # st.write("Original Delayed orders = ", delayed_orders_tmp)

    message_tmp = {"role": "assistant", "content": f"Original Total Cost = {round(value(prob_tmp.objective), 1)}  \n"
                                                   f"Original # delayed units = {round(total_delayed_units_tmp, 0)}  \n"
                                                   f"Original Delayed orders = {delayed_orders_tmp}"}
    avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message_tmp["role"], avatar=avatar):
        st.markdown(message_tmp["content"])
    # st.session_state.messages.append(message_tmp)
    placeholder_text = "Select order id..."

    all_options = [i for i in range(0, len(st.session_state.orders))]
    all_options.insert(0, placeholder_text)

    # Create a placeholder for the selectbox
    multiselect_placeholder = st.empty()

    # Render the selectbox with the default index set to 0
    selected_options = multiselect_placeholder.multiselect(
        label=placeholder_text,
        options=all_options,
        # default=[0],  # Default to the first option (placeholder_text)
        key=st.session_state.counter  # Unique key for this multiselect box
        )

    # st.write(f'option = {option}')
    # st.write(f'all_options[0] = {all_options[0]}')
    # st.write(f'st.session_state.selected_order = {st.session_state.selected_order}')

    # Check if the user has selected an order
    # Check if the user has selected any orders
    if len(selected_options) == 0 or (len(selected_options) == 1 and selected_options[0] == placeholder_text):
        st.warning("Please select at least one order to prioritize.")
        # return
        # # If the user selects the placeholder text, we treat it as no valid selection
        # st.warning("Please select at least one order to prioritize.")
    if st.button("Prioritize Selected Orders"):
        if selected_options != placeholder_text:
            st.session_state.counter+=1

            # st.write(f'User has selected {selected_options}')
            # Logic to execute when a valid order is selected
            message_tmp = {"role": "assistant", "content": f"User has selected the order(s): {selected_options}"}
            avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
            with st.chat_message(message_tmp["role"], avatar=avatar):
                st.markdown(message_tmp["content"])
            st.session_state.messages.append(message_tmp)

            # # Update session state
            # st.session_state.selected_order = option
            # # message_tmp = {"role": "assistant",
            # #                "content": f"Session state order is now order {st.session_state.selected_order}"}
            # # avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
            # # with st.chat_message(message_tmp["role"], avatar=avatar):
            # #     st.markdown(message_tmp["content"])
            #
            # prob_tmp, x_tmp, y_tmp, inv_tmp = create_model(
            #     resources=st.session_state.resources, products=st.session_state.products,
            #     customers=st.session_state.customers, orders=st.session_state.orders,
            #     time_ids=st.session_state.time_ids, min_criticality=st.session_state.min_criticality,
            #     max_criticality=st.session_state.max_criticality, seed=st.session_state.seed)
            # prob_tmp.writeLP("before.lp")
            # prob_tmp.solve()
            # orders_tmp = retrieve_fulfill_times(
            #     orders_tmp=st.session_state.orders,
            #     y_vars=y_tmp,
            #     time_periods=st.session_state.time_ids)
            # delayed_orders_tmp, total_delayed_units_tmp = check_delayed_orders(
            #     f_orders=orders_tmp, f_y=y_tmp, f_time_ids=st.session_state.time_ids)
            # st_print_product_production(
            #     f_product_ids=st.session_state.product_ids, f_resource_ids=st.session_state.resource_ids,
            #     f_x=x_tmp, f_time_ids=st.session_state.time_ids)

            # # st.write("Original Total Cost = ", round(value(prob_tmp.objective), 1))
            # # # number of delayed quantities
            # # st.write("Original Total delayed product quantity = ", round(total_delayed_units_tmp, 2))
            # # st.write("Original Delayed orders = ", delayed_orders_tmp)
            #
            # message_tmp = {"role": "assistant", "content": f"Original Total Cost = {round(value(prob_tmp.objective), 1)}  \n"
            #                                                f"Original # delayed units = {round(total_delayed_units_tmp,0)}  \n"
            #                                                f"Original Delayed orders = {delayed_orders_tmp}"}
            # avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
            # with st.chat_message(message_tmp["role"], avatar=avatar):
            #     st.markdown(message_tmp["content"])
            # st.session_state.messages.append(message_tmp)

            # # for i in range(2, 5):
            # #     for t in range(0, len(st.session_state.time_ids)):
            # #         print(f'y[{i}][{t}]{y_tmp[i][t].varValue}')
            # # st_print_product_production(
            # #     f_product_ids=st.session_state.product_ids, f_resource_ids=st.session_state.resource_ids,
            # #     f_x=x_tmp, f_time_ids=st.session_state.time_ids)
            #

            prob_tmp = add_objective_terms_v2(
                model=prob_tmp,
                order_list=[st.session_state.orders[i] for i in selected_options if i != 0],
                # order_list=[st.session_state.orders[i] for i in range(0,300)],
                multiplier=9, criticality=st.session_state.criticality,
                y_f=y_tmp,
                time_ids_f=st.session_state.time_ids)
            prob_tmp.writeLP("after.lp")
            prob_tmp.solve()
            # st_print_product_production(
            #     f_product_ids=st.session_state.product_ids, f_resource_ids=st.session_state.resource_ids,
            #     f_x=x_tmp, f_time_ids=st.session_state.time_ids)
            # # for i in range(2, 5):
            # #     for t in range(0, len(st.session_state.time_ids)):
            # #         print(f'y[{i}][{t}]{y_tmp[i][t].varValue}')
            #
            # # st.write("..retriving orders")
            orders_tmp = retrieve_fulfill_times(
                orders_tmp=st.session_state.orders,
                y_vars=y_tmp,
                time_periods=st.session_state.time_ids)
            delayed_orders_tmp, total_delayed_units_tmp = check_delayed_orders(
                f_orders=orders_tmp, f_y=y_tmp, f_time_ids=st.session_state.time_ids)
            # st_print_product_production(
            #     f_product_ids=st.session_state.product_ids, f_resource_ids=st.session_state.resource_ids,
            #     f_x=x_tmp, f_time_ids=st.session_state.time_ids)

            # st.write("Total Cost = ", round(value(prob_tmp.objective), 1))
            # # number of delayed quantities
            # st.write("Total delayed product quantity = ", round(total_delayed_units_tmp, 2))
            # st.write("Delayed orders = ", delayed_orders_tmp)
            # st.write('Prioritize order ended successfully')

            message_tmp = {"role": "assistant",
                           "content": f"New Total Cost after prioritize = {round(value(prob_tmp.objective), 1)}  \n"
                                      f"New # delayed units = {round(total_delayed_units_tmp,0)}  \n"
                                      f"New Delayed orders after prioritize = {delayed_orders_tmp}"}
            avatar = '🤖' if message_tmp["role"] == "assistant" else '👨‍💻'
            with st.chat_message(message_tmp["role"], avatar=avatar):
                st.markdown(message_tmp["content"])
            st.session_state.messages.append(message_tmp)

            # Clear the selectbox after a selection is made
            multiselect_placeholder.empty()


# def prioritize_all_orders_of_a_customer():
#     st.write('prioritize_all_orders_of_a_customer invoked successfully')


def list_orders_of_a_customer():
    st.write('list_orders_of_a_customer invoked successfully')
    st.session_state.messages.append({"role": "assistant", "content": "Invalid or in-progress module."})
def change_production_capacity_of_a_machin_resource():
    st.write('change_production_capacity_of_a_machin_resource invoked successfully')
    st.session_state.messages.append({"role": "assistant", "content": "Invalid or in-progress module."})

module_name_list = ['Initiate/create a plan',
                    'Modify the plan',
                    'Get insights',
                    'Download all results / production schedule',
                    'Prioritize orders',
                    'List orders of a customer',
                    'Change production capacity of a machine/resource '
                    ]
# module matching
module_name_mapping = {
    'Initiate/create a plan': initiate_create_plan,
    'Modify the plan': modify_plan,
    'Get insights': get_insights,
    'Download all results / production schedule': download_all_results_production_schedule,
    'Prioritize orders': prioritize_orders,
    # 'Prioritize all orders of a customer': prioritize_all_orders_of_a_customer,
    'List orders of a customer': list_orders_of_a_customer,
    'Change production capacity of a machine/resource': change_production_capacity_of_a_machin_resource
    # Add more modules as needed
    }

def extract_module_from_response(response: str):
    # st.write('  Extract module name from' + response)
    # Regex to capture the module name after "The module match is: "
    match = re.search(r"The module match is: (.+)", response)
    if match:
        # st.write('   extracted:', match.group(1))
        return match.group(1)  # Return the module name
    return None  # If no match found


# Function to extract the module from the response and map it to a function
def extract_and_invoke_module(response: str):
    # Extract the module name from the response using regex
    st.write('Extracting and invoking from text:' + response)

    module_name = extract_module_from_response(response)

    if module_name:
        # Map the user-friendly module name to the corresponding function
        if module_name in module_name_mapping:
            # Call the corresponding module function
            module_name_mapping[module_name]()  # This invokes the mapped function
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Module not found. Please try again."})
    else:
        st.session_state.messages.append(
            {"role": "assistant",
             "content": "I could not find a reasonable match, please try again or select from the list."})


def show():
    nl = '  \n'
    module_names = f"{nl}{nl.join(module_name_list)}"

    # System prompt (not displayed to the user)
    SYSTEM_PROMPT = f'''You are a specific AI assistant that try to understand what user wants and will invoke a number of modules. 
    If you find a reasonable match, I want you to respond in the format: The module match is: [Module name]
    If you cannot find a reasonable match, ask the user to try again by saying: I could not find a reasonable match, please try again or select from the list.
    You cannot respond with anything else. This is a strict requirement.
    The module names are as follows: \n
    {module_names} 
    '''
    # module_selection = st.selectbox("Select a module from the list", module_name_list)
    st.header('Interaction modules', divider=True)
    st.markdown(
        '''
        Here, the user can interact with the model by typing queries.
        
        The list of modules are on the sidebar. 
        
        Currently, **'Initiate/create a plan'** and **'Prioritize orders'** modules are active.
        
        
        '''
        )

    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
        )

    # Initialize chat history and system prompt

    if "messages" not in st.session_state:
        st.session_state.messages = []  # Start with an empty chat history
        # st.session_state.welcome_message_shown = False
    if 'chatbot_active' not in st.session_state:
        st.session_state.chatbot_active = True
    if 'selected_module' not in st.session_state:
        st.session_state.selected_module = None
    if 'selected_order' not in st.session_state:
        st.session_state.selected_order = None
    # st.write(f".........module macghing start={time.time()}")
    st.session_state.selected_order=None

    # find the models supported
    ###########################
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {st.secrets["GROQ_API_KEY"]}",
        "Content-Type": "application/json"
        }

    response = requests.get(url, headers=headers)

    import pickle
    if 'models' not in globals():
        with open('models_dict.pickle', 'rb') as handle:
            models = pickle.load(handle)

    # # Layout for model selection and max_tokens slider
    col1, col2 = st.columns(2)
    model_option = 'llama3-70b-8192'
    max_tokens = 1024

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if st.session_state.chatbot_active:
        if prompt := st.chat_input("Enter your prompt here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.selected_module = prompt
            with st.chat_message("user", avatar='👨‍💻'):
                st.markdown(prompt)

            # Fetch response from Groq API
            try:
                chat_completion = client.chat.completions.create(
                    model=model_option,
                    messages=[
                                 {"role": "system", "content": SYSTEM_PROMPT}
                                 ] + st.session_state.messages,  # Add system prompt to API context
                    max_tokens=max_tokens,
                    stream=True
                    )

                # Use the generator function with st.write_stream
                with st.chat_message("assistant", avatar="🤖"):
                    chat_responses_generator = generate_chat_responses(chat_completion)
                    full_response = st.write_stream(chat_responses_generator)
            except Exception as e:
                st.error(e, icon="🚨")

            # Append the full response to session_state.messages
            if isinstance(full_response, str):
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response})
            else:
                # Handle the case where full_response is not a string
                combined_response = "\n".join(str(item) for item in full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": combined_response})

            # # Call the function to extract and invoke the module based on the assistant's response
            st.session_state.selected_module=extract_module_from_response(full_response)
              
    print(st.session_state.selected_module)
    if st.session_state.selected_module == "Initiate/create a plan":
        initiate_create_plan()
    elif st.session_state.selected_module == 'Modify the plan':
        modify_plan()
    elif st.session_state.selected_module == 'Prioritize orders':
        # st.write(f'st.session_state.selected_order:{st.session_state.selected_order}')
        prioritize_orders()
  
        



