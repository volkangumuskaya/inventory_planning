# Import the PuLP library
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum,LpInteger,LpContinuous,LpBinary,LpStatus,value
import random
import numpy as np
from collections import defaultdict
from subpages.data_class_script_v2 import (Customer, Order, Product, Resource,
                                  generate_customers, generate_orders, generate_products, generate_resources,
                                  determine_total_quantity_per_product,print_orders,retrieve_fulfill_times)
# from subpages.inititate_planning_tool import total_delayed_units
from subpages.model_functions import print_product_production
from subpages.prioritize_order import check_delayed_orders
from subpages.model_functions import create_main_objects,create_obj_function,create_model
from subpages.prioritize_order import add_objective_terms_v2
import time
start=time.time()

#Set of periods
n_time_period=20
n_resource=2
n_customer=3
n_order=10
min_q_per_order=30
max_q_per_order=100
min_criticality=2
max_criticality=10
seed=50
random.seed(seed)


##GENERATE MAIN COMPONENTS RANDOMLY
time_ids,resources,products,customers,orders=create_main_objects(n_period= n_time_period, n_resource= n_resource, n_customer=n_customer, n_order=n_order,
                              min_q_per_order=min_q_per_order,max_q_per_order=max_q_per_order,seed=seed)
prob,x,y,inv=create_model(resources=resources, products=products, customers=customers, orders=orders,
             time_ids=time_ids, min_criticality=min_criticality, max_criticality=max_criticality,seed=seed)
prob_tmp,x_tmp,y_tmp,inv_tmp=create_model(resources=resources, products=products, customers=customers, orders=orders,
             time_ids=time_ids, min_criticality=min_criticality, max_criticality=max_criticality,seed=seed)

total_quantity_per_product=determine_total_quantity_per_product(orders_f=orders,products_f=products)
total_quantity_all_products=sum(total_quantity_per_product.values())

# Decision variables and indices
resource_ids=[x.resource_id for x in resources]
product_ids=[x.product_id for x in products]
order_ids=[x.order_id for x in orders]

random.seed(seed)
criticality=[random.randint(a=min_criticality,b=max_criticality)/max_criticality for x in orders]

#Write LPs
prob.writeLP("nxp_v3.lp")
prob_tmp.writeLP("nxp_v3_tmp.lp")
prob.writeMPS("nxp_v3.mps")

# The problem is solved using PuLP's choice of Solver
prob.solve()
end=time.time()

#retrieve fulfillment times
orders=retrieve_fulfill_times(orders_tmp=orders,y_vars=y,time_periods=time_ids)
delayed_orders,total_delayed_units=check_delayed_orders(f_orders=orders, f_y=y, f_time_ids=time_ids)

#print production
print_product_production(f_product_ids=product_ids,f_resource_ids=resource_ids,f_x=x,f_time_ids=time_ids)

print(f'Used seed:{seed}')
# n variables
print("# variables = ", len(prob.variables()))
# The optimised objective function value is printed to the screen
print("# constraints = ", len(prob.constraints))
# The optimised objective function value is printed to the screen
print("Total Cost = ", value(prob.objective))
# number of delayed quantities
print("Total delayed product quantity:", total_delayed_units)
print("Total quantity:", total_quantity_all_products)
print(f'% delayed items: %{round(total_delayed_units/total_quantity_all_products*100,2)}')
# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])
print("Time total:",end-start)

#Create df s
order_df=pd.DataFrame([(obj.order_id,
                        obj.customer_name,
                        obj.deadline,
                        obj.product_id,
                        obj.product[obj.product_id],
                        criticality[obj.order_id],
                        obj.fulfilled) for obj in orders],
                      columns=['Order_ID', 'Customer_Name', 'Deadline', 'Product_ID','Product_Amount','Criticality','Fulfilled_time'])
order_df['Delay_status'] = np.where(order_df['Fulfilled_time']>order_df['Deadline'], 'Delayed', 'On_time')
order_df['Delay_duration'] = np.where(order_df['Fulfilled_time']>order_df['Deadline'], order_df['Fulfilled_time']>order_df['Deadline'], 0)


def summarize_plan(df: pd.DataFrame) -> pd.DataFrame:
    n_delayed=(order_df.Delay_duration > 0).sum()
    n_on_time = (order_df.Delay_duration <= 0).sum()
    tmp=(f'The plan is made for {len(df)} orders\n'
         f'# of On time:{n_on_time} -(%{n_on_time/len(df)*100:.2f})\n'
         f'# of Delayed:{n_delayed} -(%{n_delayed/len(df)*100:.2f})\n'
         )
    return tmp

print(summarize_plan(order_df))



# st.write("Used seed:",seed)
# # n variables
# st.write("Number of variables = ", len(prob.variables()))
# # The optimised objective function value is st.writeed to the screen
# st.write("Number of constraints = ", len(prob.constraints))
# # The optimised objective function value is st.writeed to the screen
# st.write("Total Cost = ", round(value(prob.objective),1))
# # number of delayed quantities
# st.write("Total delayed product quantity = ", round(total_delayed_units,2))
# st.write("Total quantity = ", total_quantity_all_products)
# st.write("%Delayed items = %", round(total_delayed_units/total_quantity_all_products*100,2))
# # The status of the solution is st.writeed to the screen
# st.write("Status:", LpStatus[prob.status])
# st.write("Time total:",round(end-start,2))
#


print(prob_tmp.objective)
print(value(prob_tmp.objective))
prob_tmp=add_objective_terms_v2(model=prob_tmp,order_list=orders[0:1],multiplier=30,criticality=criticality,y_f=y_tmp,time_ids_f=time_ids)
prob_tmp.solve()

orders_tmp=retrieve_fulfill_times(orders_tmp=orders,y_vars=y_tmp,time_periods=time_ids)
delayed_orders_tmp,total_delayed_units_tmp=check_delayed_orders(f_orders=orders_tmp, f_y=y_tmp, f_time_ids=time_ids)
print_product_production(f_product_ids=product_ids,f_resource_ids=resource_ids,f_x=x_tmp,f_time_ids=time_ids)

# 21.9*1.5
# # Create new terms
# new_term = [99 * (t - o.deadline) ** 2 * criticality[o.order_id] * y[o.order_id][t] * o.product[o.product_id]
#             for o in orders[7:8] for t in time_ids if t > o.deadline]
#
# new_term2 = [99 * (t - o.deadline) ** 2 *  criticality[o.order_id] * y[o.order_id][t] * o.product[o.product_id]
#             for o in orders[1:2] for t in time_ids if t > o.deadline]
#
#
# prob_copy = prob.copy()
# prob_copy.setObjective(lpSum(prob_copy.objective + new_term))
# #
# prob_copy2 = prob_copy.copy()
# prob_copy2.setObjective(lpSum(prob_copy2.objective + new_term2))
# 32.84*1.5
#
# print(prob.objective)
# print(prob_copy.objective)
# print(prob_copy2.objective)
# #
# prob.solve()
# delayed_orders=[]
# for o in orders:
#     for t in time_ids:
#         check_sum=0
#         if (y[o.order_id][t].varValue>0.001)&(check_sum<=1.00):
#             check_sum+=o.deadline
#             if t>o.deadline:
#                 total_delayed_units+=o.product[o.product_id]*y[o.order_id][t].varValue
#                 print(f'order:{o.order_id},deadline:{o.deadline},product:{o.product_id},var:{y[o.order_id][t]},q:{o.product[o.product_id]},val:{y[o.order_id][t].varValue}')
#                 delayed_orders.append(o.order_id)
# set(delayed_orders)
# #
# prob_copy.solve()
# delayed_orders_copy=[]
# for o in orders:
#     for t in time_ids:
#         check_sum=0
#         if (y[o.order_id][t].varValue>0.001)&(check_sum<=1.00):
#             check_sum+=o.deadline
#             if t>o.deadline:
#                 total_delayed_units+=o.product[o.product_id]*y[o.order_id][t].varValue
#                 print(f'order:{o.order_id},deadline:{o.deadline},product:{o.product_id},var:{y[o.order_id][t]},q:{o.product[o.product_id]},val:{y[o.order_id][t].varValue}')
#                 delayed_orders_copy.append(o.order_id)
# set(delayed_orders_copy)
# #
# # prob_copy2.solve()
# # delayed_orders_copy2=[]
# # for o in orders:
# #     for t in time_ids:
# #         check_sum=0
# #         if (y[o.order_id][t].varValue>0.001)&(check_sum<=1.00):
# #             check_sum+=o.deadline
# #             if t>o.deadline:
# #                 total_delayed_units+=o.product[o.product_id]*y[o.order_id][t].varValue
# #                 print(f'order:{o.order_id},deadline:{o.deadline},product:{o.product_id},var:{y[o.order_id][t]},q:{o.product[o.product_id]},val:{y[o.order_id][t].varValue}')
# #                 delayed_orders_copy2.append(o.order_id)
#
# # set(delayed_orders)
# # set(delayed_orders_copy)
# # set(delayed_orders_copy2)
#
#
# def add_objective_terms(model: LpProblem, order_list: list[Order], multiplier: float,criticality:list[float]):
#     new_term = [multiplier * (t - o.deadline) ** 2 * criticality[o.order_id] * y[o.order_id][t] * o.product[o.product_id]
#                 for o in order_list for t in time_ids if t > o.deadline]
#     model_copy = model.copy()
#     # Set the new objective back to the model
#     model_copy.setObjective(lpSum(model_copy.objective + new_term))
#     return model_copy
#
# prob_tmp=add_objective_terms(model=prob_tmp,order_list=orders[6:8],multiplier=0.5,criticality=criticality)
#
# print(prob_tmp.objective)
# print(prob.objective)
#
# prob.solve()
# prob_tmp.solve()