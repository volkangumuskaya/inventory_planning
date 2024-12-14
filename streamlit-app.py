import streamlit as st
import random
from subpages import inititate_planning_tool, module_matching, model_v2, default_model
from subpages.data_class_script_v2 import (Customer, Order, Product, Resource,
                                            generate_customers, generate_orders, generate_products, generate_resources,
                                            determine_total_quantity_per_product, print_orders, retrieve_fulfill_times)
from subpages.model_functions import print_product_production, create_main_objects, create_obj_function, create_model
from subpages.prioritize_order import check_delayed_orders, add_objective_terms_v2
import test

# Set up the page configuration
st.set_page_config(
    page_title='volkan-ai',
    layout="wide"
)

# Set random seed for reproducibility
seed = 50
random.seed(seed)

# Parameters
n_time_period = 20
n_resource = 2
n_customer = 3
n_order = 500
min_q_per_order = 40
max_q_per_order = 70
min_criticality = 4
max_criticality = 10

# Generate main components randomly
time_ids, resources, products, customers, orders = create_main_objects(
    n_period=n_time_period, 
    n_resource=n_resource, 
    n_customer=n_customer, 
    n_order=n_order,
    min_q_per_order=min_q_per_order, 
    max_q_per_order=max_q_per_order, 
    seed=seed
)

# Create models
prob, x, y, inv = create_model(
    resources=resources, 
    products=products, 
    customers=customers, 
    orders=orders,
    time_ids=time_ids, 
    min_criticality=min_criticality, 
    max_criticality=max_criticality, 
    seed=seed
)
prob_tmp, x_tmp, y_tmp, inv_tmp = create_model(
    resources=resources, 
    products=products, 
    customers=customers, 
    orders=orders,
    time_ids=time_ids, 
    min_criticality=min_criticality, 
    max_criticality=max_criticality, 
    seed=seed
)

# Solve the problem
prob.solve()

# Retrieve fulfill times and check delayed orders
orders = retrieve_fulfill_times(orders_tmp=orders, y_vars=y, time_periods=time_ids)
delayed_orders, total_delayed_units = check_delayed_orders(f_orders=orders, f_y=y, f_time_ids=time_ids)

# Determine total quantity per product
total_quantity_per_product = determine_total_quantity_per_product(orders_f=orders, products_f=products)
total_quantity_all_products = sum(total_quantity_per_product.values())

# Prepare decision variables and indices
resource_ids = [x.resource_id for x in resources]
product_ids = [x.product_id for x in products]
order_ids = [x.order_id for x in orders]
resource_names = [x.name for x in resources]
product_names = [x.name for x in products]
order_names = [f'order_{x.order_id}' for x in orders]

# Set random criticality for each order
criticality = [random.randint(min_criticality, max_criticality) / max_criticality for x in orders]

# Save to session state
st.session_state.model_data = {
    'current_model': prob,
    'orders': orders,
    'delayed_orders': delayed_orders,
    'total_delayed_units': total_delayed_units,
    'resources': resources,
    'products': products,
    'product_ids': product_ids,
    'order_ids': order_ids,
    'resource_ids': resource_ids,
    'seed': seed,
    'min_criticality': min_criticality,
    'max_criticality': max_criticality,
    'customers': customers,
    'time_ids': time_ids,
    'x': x,
    'y': y,
    'criticality': criticality,
    'tmp_model': prob_tmp
}

# Sidebar navigation options
module_name_list = [
    'Initiate/create a plan',
    'Modify the plan',
    'Get insights',
    'Download all results / production schedule',
    'Prioritize orders',
    'List orders of a customer',
    'Change production capacity of a machine/resource'
]

# Sidebar setup
st.sidebar.header("**NAVIGATION**")
page = st.sidebar.radio("", ['Default model', "Module matching", "Model v2", "test"])

# Handle page navigation
pages = {
    "Model v2": model_v2.show,
    "Default model": default_model.show,
    "Module matching": module_matching.show,
    "test": test.show_test
}

# Display the selected page content
pages.get(page, lambda: st.write("Page not found"))()

# Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []  # Start with an empty chat history
    st.session_state.welcome_message_shown = False
