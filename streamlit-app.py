import streamlit as st
from streamlit import divider
st.set_page_config(
    page_title='volkan-ai',
    layout="wide"
)
from subpages import inititate_planning_tool
from subpages import module_matching
from subpages import model_v2
from subpages import default_model
import test

import streamlit as st

import random
from subpages.data_class_script_v2 import (Customer, Order, Product, Resource,
                                  generate_customers, generate_orders, generate_products, generate_resources,
                                  determine_total_quantity_per_product,print_orders,retrieve_fulfill_times)
from subpages.model_functions import print_product_production
from subpages.prioritize_order import check_delayed_orders
from subpages.model_functions import create_main_objects,create_obj_function,create_model
from subpages.prioritize_order import add_objective_terms_v2


#Set of periods
n_time_period=20
n_resource=2
n_customer=3
n_order=500
min_q_per_order=40
max_q_per_order=70
min_criticality=4
max_criticality=10
seed=50
random.seed(seed)


st.write('after page config')
##GENERATE MAIN COMPONENTS RANDOMLY
time_ids, resources, products, customers, orders = create_main_objects(
    n_period=n_time_period, n_resource=n_resource, n_customer=n_customer, n_order=n_order,
    min_q_per_order=min_q_per_order, max_q_per_order=max_q_per_order, seed=seed)
prob, x, y, inv = create_model(
    resources=resources, products=products, customers=customers, orders=orders,
    time_ids=time_ids, min_criticality=min_criticality, max_criticality=max_criticality, seed=seed)
prob_tmp, x_tmp, y_tmp, inv_tmp = create_model(
    resources=resources, products=products, customers=customers, orders=orders,
    time_ids=time_ids, min_criticality=min_criticality, max_criticality=max_criticality, seed=seed)
prob.solve()
st.write('after solve')
orders = retrieve_fulfill_times(
        orders_tmp=orders,
        y_vars=y,
        time_periods=time_ids)
delayed_orders, total_delayed_units = check_delayed_orders(
        f_orders=orders, f_y=y, f_time_ids=time_ids)

total_quantity_per_product = determine_total_quantity_per_product(orders_f=orders, products_f=products)
total_quantity_all_products = sum(total_quantity_per_product.values())

# Decision variables and indices
resource_ids = [x.resource_id for x in resources]
product_ids = [x.product_id for x in products]
order_ids = [x.order_id for x in orders]
resource_names = [x.name for x in resources]
product_names = [x.name for x in products]
order_names = [f'order_{x.order_id}' for x in orders]
random.seed(seed)
criticality = [random.randint(a=min_criticality, b=max_criticality) / max_criticality for x in orders]

#Save to session state
st.session_state.current_model = prob
st.session_state.orders = orders
st.session_state.delayed_orders = delayed_orders
# st.write('init entered')
st.session_state.total_delayed_units = total_delayed_units
st.session_state.resources = resources
st.session_state.products = products
st.session_state.product_ids = product_ids
st.session_state.order_ids = order_ids
st.session_state.resource_ids = resource_ids
st.session_state.seed=seed
st.session_state.min_criticality=min_criticality
st.session_state.max_criticality=max_criticality

st.session_state.customers = customers
st.session_state.time_ids = time_ids
st.session_state.x = x
st.session_state.y = y
st.session_state.criticality = criticality

# st.write("st.session_state.current_model initialized")
st.session_state.tmp_model = prob_tmp
# st.write("st.session_state.tmp_model initialized")


# Set the title and favicon that appear in the Browser's tab bar.
module_name_list = ['Initiate/create a plan',
                    'Modify the plan',
                    'Get insights',
                    'Download all results / production schedule',
                    'Prioritize orders',
                    # 'Prioritize all orders of a customer',
                    'List orders of a customer',
                    'Change production capacity of a machine/resource '
                    ]

# Sidebar navigation
# st.sidebar.title("Navigation",divider=True)
st.sidebar.header("**NAVIGATION**",divider=True)

page = st.sidebar.radio(
    "",
    # ["Model v1",'Model v2','Module v2.2',"Module matching",'test']
    ['Default model',"Module matching"]
)

# import os
# print("Main Current Working Directory:", os.getcwd())
# Initialize chat history and system prompt
if "messages" not in st.session_state:
  st.session_state.messages = []  # Start with an empty chat history
  st.session_state.welcome_message_shown = False

if page == "Model v2":
    st.header("Model v2",divider=True)
    model_v2.show()
elif page == "Default model":
    # st.header("Default model",divider=True)
    # st.sidebar.title("Module list")
    # module_selection = st.selectbox("Select a module from the list", module_name_list)

    default_model.show()
elif page == "Module matching":
    # st.sidebar.markdown("### Modules Available:")
    st.sidebar.header("Module list",divider=True)
    # st.sidebar.markdown("### Modules Available:")
    st.sidebar.text("\n".join(module_name_list))
    module_matching.show()
elif page=='test':
    st.header("Module matching", divider=True)
    test.show_test()
# elif page == "Contact":
#     test_page.show()

