# This script is run under the hood to initiate the session states.
# Observe that in subpages.module_matching, we use st.session_state vars without initializing them.
# If we run default_model page, there we do initialize. However, even if we activate module_matching straight away
# these vars are already initialized, for example st.session_state.min_criticality.
# It is also where we format the streamlit page via st.set_page_config (st.set_page_config should always be the first
# streamlit command ti be run. If we added a st.write('hello') before st.set_page_config, we would get errror).
# If interested, some st.write's can be thrown in various points to check the order of execution.

import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
st.write('checkpoint1 initialize.py')
import random
st.write('checkpoint2 initalize')
from subpages.classes_and_generating_functions import (Customer, Order, Product, Resource,
                                                       generate_customers, generate_orders, generate_products,
                                                       generate_resources,
                                                       determine_total_quantity_per_product, print_orders,
                                                       retrieve_fulfill_times, create_main_objects)
st.write('checkpoint3 initalize')
from subpages.model_functions import print_product_production, add_objective_terms_v2, check_delayed_orders
st.write('checkpoint4 initalize')
from subpages.model_functions import create_obj_function,create_model
st.write('checkpoint5 initalize')
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

def initial_run(): 
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
  st.write('customers initalized')
  st.session_state.time_ids = time_ids
  st.session_state.x = x
  st.session_state.y = y
  st.session_state.criticality = criticality
  st.session_state.tmp_model = prob_tmp
