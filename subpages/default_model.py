# Import the PuLP library
import streamlit as st
from pulp import LpProblem, LpMinimize, LpStatus,value
import time


from subpages.model_functions import create_model,check_delayed_orders
from subpages.classes_and_generating_functions import (determine_total_quantity_per_product,
                                                       retrieve_fulfill_times, create_main_objects)


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

    # Set the title and explanation that appears at the top of the page.
    st.header('A multi-horizon planning tool v2', divider=True)
    st.markdown(
    '''
    This is the second model to create and solve an inventory planning problem with time periods. 
    
    Press 'Build' to generate a new model and solve. Scroll down to see results. 
    
    If needed, modify the parameters and press 'Build' to generate a new model. 
    '''
        )

    # Create the widgets that control the problem parameters
    st.header('Problem parameters', divider=True)
    # Create three columns with custom widths
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Number of time periods")
        n_time_period = st.selectbox('#Time periods', list(range(10, 21)), index=10)
        st.subheader("Resources")
        n_resource = st.selectbox('#Resources', list(range(2, 3)), index=0)
        n_customer = st.selectbox('#Customer', list(range(3, 4)), index=0)
    with col2:
        st.subheader("Orders")
        n_order = st.select_slider(
            "Select number of orders",
            options=list([50,500, 1000, 1500, 2000]),
            value=500,
            )
        min_q_per_order, max_q_per_order = st.select_slider(
            "Select min/max resources needed per product",
            options=[20, 30, 40, 50, 60, 70, 80, 90, 100],
            value=(40, 70),
            )

    min_criticality = 4
    max_criticality = 10

    # Create three columns with custom widths
    col1, col2 = st.columns([1, 0.001])
    print(f'n_time_period: {n_time_period}')
    with col1:
        if st.button("BUILD MODEL", type="primary"):
            start = time.time()
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

            #Save to session state. A dict could be used
            st.session_state.current_model = prob
            st.session_state.tmp_model = prob_tmp
            st.session_state.resources=resources
            st.session_state.products=products
            st.session_state.orders=orders
            st.session_state.time_ids=time_ids
            st.session_state.min_criticality=min_criticality
            st.session_state.max_criticality=max_criticality
            st.session_state.min_quantity=min_q_per_order
            st.session_state.max_quantity=max_q_per_order

            # The problem is solved using PuLP's choice of Solver
            prob.solve()
            orders = retrieve_fulfill_times(orders_tmp=orders, y_vars=y, time_periods=time_ids)
            delayed_orders, total_delayed_units = check_delayed_orders(f_orders=orders, f_y=y, f_time_ids=time_ids)
            st.session_state.current_model = prob
            st.session_state.orders = orders
            st.session_state.delayed_orders = delayed_orders

            end = time.time()

            avatar = '🤖'
            with st.chat_message("assistant", avatar=avatar):
                st.markdown(f"**Delayed orders:** {delayed_orders}")
                st.markdown(f"**Total # of delayed products :** {round(total_delayed_units, 0)}")
                st.markdown(f"**Total # of products:** {total_quantity_all_products}")
                st.markdown(f"**%Delayed items:** {round(total_delayed_units / total_quantity_all_products * 100, 2)}%")
                st.markdown(f"**Total Cost:** {round(value(prob.objective), 1)}")
                st.markdown(f"**Number of variables:** {len(prob.variables())}")
                st.markdown(f"**Number of constraints:** {len(prob.constraints)}")
                st.markdown(f"**Status:** {LpStatus[prob.status]}")
                st.markdown(f"**Time total:** {round(end - start, 2)} seconds")


