#This script includes the helper functions related to building or modifying math model
import random
import streamlit as st

from subpages.classes_and_generating_functions import (Customer, Order, Product, Resource,
                                                       determine_total_quantity_per_product)
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpContinuous

def create_obj_function(problem: LpProblem, y: LpVariable, criticality: list[float], orders: list[Order],
                        time_ids: list[int]):
    obj_func_production = [(t - o.deadline) ** 2 * criticality[o.order_id] * y[o.order_id][t] * o.product[o.product_id]
                           for o in orders for t in time_ids if t > o.deadline]
    problem += (lpSum(obj_func_production))
    return problem

def print_product_production(f_product_ids:list[int],f_resource_ids:list[int],f_time_ids:list[int],f_x:LpVariable) -> None:
    for p in f_product_ids:
        for r in f_resource_ids:
            print(f'Product {p} Resource {r} : {[round(f_x[p][r][t].varValue,0) for t in f_time_ids]}' )

def st_print_product_production(f_product_ids:list[int],f_resource_ids:list[int],f_time_ids:list[int],f_x:LpVariable) -> None:
    for p in f_product_ids:
        for r in f_resource_ids:
            st.write(f'Product {p} Resource {r} : {[round(f_x[p][r][t].varValue,0) for t in f_time_ids]}' )

def create_model(resources: list[Resource] , products : list[Product], customers : list[Customer], orders : list[Order],
                 time_ids:list[int],
                 min_criticality:int , max_criticality:int, seed:int):

    resource_ids = [x.resource_id for x in resources]
    product_ids = [x.product_id for x in products]
    order_ids = [x.order_id for x in orders]
    resource_names = [x.name for x in resources]
    product_names = [x.name for x in products]
    order_names = [f'order_{x.order_id}' for x in orders]
    random.seed (seed)
    print(random.seed)
    criticality = [random.randint(a=min_criticality, b=max_criticality) / max_criticality for x in orders]
    print(f'Criticality: {criticality[0:10]}')
    total_quantity_per_product = determine_total_quantity_per_product(orders_f=orders, products_f=products)
    total_quantity_all_products = sum(total_quantity_per_product.values())

    capacities = [round(total_quantity_all_products / len(time_ids) / len(resources), 0) + 1 for x in resources]

    # BUILD MODEL
    # Decision vars
    # X: amount produced of resource R in time T
    x = LpVariable.dicts(
        name="production_p_r_t", indices=(product_ids, resource_ids, time_ids), lowBound=0, upBound=None,
        cat=LpContinuous)
    # Y: 1 if order O is fulfilled in time T. We allow only complete fulfillment of orders/delivery
    y = LpVariable.dicts(
        name="order_fulfill_o_t", indices=(order_ids, time_ids), lowBound=0, upBound=1, cat=LpContinuous)
    # starting inventory of resource R in time T
    inv = LpVariable.dicts(
        name="starting_inventory_p_t", indices=(product_ids, time_ids + [len(time_ids)]),
        lowBound=0, upBound=None, cat=LpContinuous)

    # Create initial model
    prob = LpProblem("NXP_trial_v3", LpMinimize)

    # The objective function consists of resource and delay costs
    obj_func_production = [(t - o.deadline) ** 2 * criticality[o.order_id] * y[o.order_id][t] * o.product[o.product_id]
                           for o in orders for t in time_ids if t > o.deadline]
    prob += (lpSum(obj_func_production))

    # CONSTRAINTS
    # order fulfillment
    for o in orders:
        prob += (lpSum([y[o.order_id][t] for t in time_ids]) == 1,
                 f"Order_fulfill_order{o.order_id}")

    # Resource capacity constraints
    for t in time_ids:
        for r in resource_ids:
            prob += (lpSum([p.resource_usage[r] * x[p.product_id][r][t] for p in products]) <= capacities[r],
                     f"Capacity_resource{r}_time{t}")

    # Starting inventory is 0
    for p in product_ids:
        prob += (inv[p][0] <= 0), f"initial_starting_inventory_product{p}"

    # starting inventory + production  - resource needed to fulfill orders = ending inventory
    for t in time_ids:
        for p in product_ids:
            prob += (
                lpSum([x[p][r][t] for r in resource_ids]) -
                lpSum([o.product[p] * y[o.order_id][t] for o in orders]) +
                inv[p][t] == inv[p][t + 1],
                f"Inventory_balance_product{p}_time{t}",
                )
    return prob,x,y,inv


def add_objective_terms_v2(model: LpProblem, order_list: list[Order],y_f:list,
                           multiplier: float, criticality:list[float], time_ids_f:list[int]):
    """
        Add new terms to the objective function to prioritize the selected orders (order_list)
    """
    new_term = [
        multiplier * (t - o.deadline) ** 2 * criticality[o.order_id] * y_f[o.order_id][t] * o.product[o.product_id]
        for o in order_list for t in time_ids_f if t > o.deadline]
    model_copy = model.copy()

    model_copy.setObjective(lpSum(model_copy.objective + new_term))
    return model_copy


def check_delayed_orders(f_orders:list[Order], f_y:LpVariable, f_time_ids: list[int]):
    """
    Create set of delayed orders that will be displayed for user reference
    """

    # Each variable printed
    total_delayed_units=0
    delayed_orders=[]
    for o in f_orders:
        for t in f_time_ids:
            check_sum=0
            if (f_y[o.order_id][t].varValue>0.0001) and (check_sum<=1.00):
                check_sum+=f_y[o.order_id][t].varValue
                if t>o.deadline:
                    total_delayed_units+=o.product[o.product_id]*f_y[o.order_id][t].varValue
                    print(f'order:{o.order_id},deadline:{o.deadline},'
                          f'product:{o.product_id},var:{f_y[o.order_id][t]},'
                          f'delay_q:{o.product[o.product_id]*f_y[o.order_id][t].varValue}, sum:{check_sum},'
                          f'q:{o.product[o.product_id]},val:{o.product[o.product_id]*f_y[o.order_id][t].varValue},'
                          f'total_delay:{total_delayed_units}')
                    delayed_orders.append(o.order_id)
    return sorted(set(delayed_orders)), total_delayed_units
