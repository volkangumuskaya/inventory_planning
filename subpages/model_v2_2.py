# Import the PuLP library
import streamlit as st
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum,LpInteger,LpContinuous,LpBinary,LpStatus,value
import random
import numpy as np
from collections import defaultdict
import pickle
import os
import sys
from pathlib import Path
import time
from subpages.prioritize_order import check_delayed_orders,add_objective_terms_v2
start=time.time()

sys.path.append(str(Path(__file__).parent))
from subpages.model_functions import print_product_production,st_print_product_production
from subpages.model_functions import create_main_objects,create_obj_function,create_model
from subpages.data_class_script_v2 import (Customer, Order, Product, Resource,
                                  generate_customers, generate_orders, generate_products, generate_resources,
                                  determine_total_quantity_per_product,print_orders,retrieve_fulfill_times)

def check_delayed_orders(f_orders: list[Order], f_y: LpVariable, f_time_ids: list[int]):
    # Each variable printed
    total_delayed_units = 0
    delayed_orders = []
    for o in f_orders:
        for t in f_time_ids:
            check_sum = 0
            if (f_y[o.order_id][t].varValue > 0.001) and (check_sum <= 1.00):
                check_sum += o.deadline
                if t > o.deadline:
                    total_delayed_units += o.product[o.product_id] * f_y[o.order_id][t].varValue
                    print(
                        f'order:{o.order_id},deadline:{o.deadline},product:{o.product_id},'
                        f'var:{f_y[o.order_id][t]},q:{o.product[o.product_id]},val:{f_y[o.order_id][t].varValue}')
                    delayed_orders.append(o.order_id)
    return set(delayed_orders), total_delayed_units

def show():
    # Initialize session state for the button click
    if "show_solve_section" not in st.session_state:
        st.session_state.show_solve_section = False
    if "show_build_section" not in st.session_state:
        st.session_state.show_build_section = False
    if "show_output_section" not in st.session_state:
        st.session_state.show_output_section = False
    if "current_model" not in st.session_state:
        st.session_state.current_model = LpProblem("current_model", LpMinimize)
    if "tmp_model" not in st.session_state:
        st.session_state.tmp_model = LpProblem("tmp_model", LpMinimize)

    # Set the title that appears at the top of the page.
    # st.image('images/el-chalten-min.jpg', 'El Chalten, Patagonia')
    st.header('A multi-horizon planning tool v2', divider=True)
    '''
    This is the second model to create and solve an inventory planning problem with time periods. Enter problem parameters and press 'Build' to generate a model. Upon doing so, you may download the model as txt file and 'Solve'.
    '''

    # Show measurements only for selected station
    st.header('Problem parameters', divider=True)
    # Create three columns with custom widths
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Number of time periods")
        n_time_period = st.selectbox('#Time periods', list(range(10, 21)), index=0)
        time_ids = list(range(n_time_period))
        st.subheader("Resources")
        n_resource = st.selectbox('#Resources', list(range(2, 3)), index=0)
        n_customer = st.selectbox('#Customer', list(range(3, 4)), index=0)
    with col2:
        st.subheader("Orders")
        n_order = st.select_slider(
            "Select number of orders",
            options=list([500, 1000, 1500, 2000]),
            value=1000,
            )
        min_q_per_order, max_q_per_order = st.select_slider(
            "Select min/max resources needed per product",
            options=[20, 30, 40, 50, 60, 70, 80, 90, 100],
            value=(50, 100),
            )

    min_criticality = 4
    max_criticality = 10

    # Create three columns with custom widths
    col1, col2 = st.columns([1, 0.001])
    with col1:
        if st.button("BUILD MODEL", type="primary"):
            try:
                seed = 50
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
                st.write("st.session_state.current_model initialized")
                st.session_state.tmp_model = prob_tmp
                st.write("st.session_state.tmp_model initialized")
                st.session_state.resources=resources
                st.session_state.products=products
                st.session_state.orders=orders
                st.session_state.time_ids=time_ids
                st.session_state.min_criticality=min_criticality
                st.session_state.max_criticality=max_criticality
                st.session_state.min_quantity=min_q_per_order
                st.session_state.max_quantity=max_q_per_order


                # Download model
                with open("nxp_v3.lp", "rb") as file:
                    btn = st.download_button(
                        label="Download model",
                        data=file,
                        file_name="nxp_v3.lp"
                        )

                # The problem is solved using PuLP's choice of Solver
                prob.solve()
                prob.writeLP("original.lp")
                orders = retrieve_fulfill_times(orders_tmp=orders, y_vars=y, time_periods=time_ids)
                delayed_orders, total_delayed_units = check_delayed_orders(f_orders=orders, f_y=y, f_time_ids=time_ids)
                # print_product_production(
                #     f_product_ids=product_ids, f_resource_ids=resource_ids, f_x=x, f_time_ids=time_ids)
                st_print_product_production(
                    f_product_ids=product_ids, f_resource_ids=resource_ids, f_x=x, f_time_ids=time_ids)
                end = time.time()

                st.write("Used seed:", seed)
                # n variables
                st.write("Number of variables = ", len(prob.variables()))
                # The optimised objective function value is st.writeed to the screen
                st.write("Number of constraints = ", len(prob.constraints))
                # The optimised objective function value is st.writeed to the screen
                st.write("Total Cost = ", round(value(prob.objective), 1))
                # number of delayed quantities
                st.write("Total delayed product quantity = ", round(total_delayed_units, 2))
                st.write("Delayed orders = ", delayed_orders)
                st.write("Total quantity = ", total_quantity_all_products)
                st.write("%Delayed items = %", round(total_delayed_units / total_quantity_all_products * 100, 2))
                # The status of the solution is st.writeed to the screen
                st.write("Status:", LpStatus[prob.status])
                st.write("Time total:", round(end - start, 2))


                # st.write("STARTING MODIFY")
                # prob_tmp = add_objective_terms_v2(
                #     model=prob_tmp, order_list=orders[0:400], multiplier=10, criticality=criticality, y_f=y_tmp,
                #     time_ids_f=time_ids)
                # st.write("solving")
                # prob_tmp.solve()
                # st.write("retriving orders")
                # orders_tmp = retrieve_fulfill_times(orders_tmp=orders, y_vars=y_tmp, time_periods=time_ids)
                # delayed_orders_tmp, total_delayed_units_tmp = check_delayed_orders(
                #     f_orders=orders_tmp, f_y=y_tmp, f_time_ids=time_ids)
                # st_print_product_production(
                #     f_product_ids=product_ids, f_resource_ids=resource_ids, f_x=x_tmp, f_time_ids=time_ids)
                # st.write("Total Cost = ", round(value(prob_tmp.objective), 1))
                # # number of delayed quantities
                # st.write("Total delayed product quantity = ", round(total_delayed_units_tmp, 2))
                # st.write("Delayed orders = ", delayed_orders_tmp)
            except:
                st.write('Error')


