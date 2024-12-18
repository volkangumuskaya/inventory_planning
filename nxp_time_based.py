# Import the PuLP library
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum,LpInteger,LpContinuous,LpBinary,LpStatus,value
import random
from collections import defaultdict
random.seed(42)

from subpages.data_class_script_v2  import Customer, Order, Product, Resource, generate_customers, generate_orders, generate_products, generate_resources

#Set of periods
time_ids=[0,1,2]
unit_delay_cost=10000

##GENERATE MAIN COMPONENTS RANDOMLY
resources=generate_resources(n_resources=2) #generate resource types
#generate products randomly. Each product requires random type of resources (one or multiple) and random amounts from 0-20
products=generate_products(n_products=5,resources=resources, min_resource_needed=0, max_resource_needed=20)
customers=generate_customers(n_customers=3)
#generate orders randomly. One order consists of 2-4 types of products and 10-20 units for each
orders=generate_orders(n_orders=30,products=products,customers=customers,time_periods=time_ids,
                       min_product_type=2,max_product_type=4,
                       min_product_amt=10,max_product_amt=20)

#Calculate total resource for all orders in order to set capacities that will force some delays/avoid trivial solutions
total_resource_needed=defaultdict(int)
for o in orders:
    for r_id,r in enumerate(resources):
        total_resource_needed[r_id]+=o.total_resource_usage[r_id]

# Decision variables and indices
resource_ids=[x.resource_id for x in resources]
order_ids=[x.order_id for x in orders]

delay_costs=[unit_delay_cost for x in orders]

resource_names=[x.name for x in resources]
resource_costs=[random.randint(a=2,b=8)/10 for _ in resources]
resource_capacities=[round(total_resource_needed[r]*0.85/len(time_ids),0) for r in resource_ids]

#BUILD MODEL
#Decision vars
# X: amount produced of resource R in time T
x = LpVariable.dicts(name="resource_production", indices=(resource_ids,time_ids),lowBound= 0,upBound= None,cat=LpContinuous)
# Y: 1 if order O is fulfilled in time T. We allow only complete fulfillment of orders/delivery
y = LpVariable.dicts(name="order_fulfillment", indices=(order_ids,time_ids),lowBound= 0,upBound= None,cat=LpBinary)
# 1 if order O is delayed in time T
order_delay = LpVariable.dicts(name="order_delay", indices=(order_ids,time_ids),lowBound= 0,upBound= None,cat=LpBinary)
# starting inventory of resource R in time T
inv = LpVariable.dicts(name="starting_inventory", indices=(resource_ids,time_ids+[len(time_ids)]),
                       lowBound= 0,upBound= None,cat=LpContinuous)

# Create initial model
prob = LpProblem("NXP_trial", LpMinimize)

# The objective function consists of resource and delay costs
obj_func_production=[x[r][t]*resource_costs[r] for t in time_ids for r in resource_ids ]
obj_func_delay_cost=[(order_delay[o][t])*delay_costs[o] for t in time_ids for o in order_ids if t>=orders[o].deadline]

prob += (
    lpSum(obj_func_production+obj_func_delay_cost)
)

#CONSTRAINTS
# Resource capacity constraints
for t in time_ids:
    for r in resource_ids:
        prob += (x[r][t] <= resource_capacities[r],f'Resource_cap_{resource_names[r]}_time_{t}')

# Starting inventory is 0
for r in resource_ids:
    prob += (inv[r][0] <= 0)

# starting inventory + production  - resource needed to fulfill orders = ending inventory
for t in time_ids:
    for r in resource_ids:
        prob += (
            lpSum([orders[o].total_resource_usage[r]*y[o][t] for o in order_ids])-x[r][t]-inv[r][t] == -inv[r][t+1],
            f"Order_fulfill_{r}_{t}",
        )

#Delay=1 if order not fulfilled at deadline T or the following periods
for o in order_ids:
    for t in time_ids:
        if t>=orders[o].deadline:
            prob += (
                lpSum([y[o][t_s] for t_s in time_ids if t_s<=t]) + order_delay[o][t] >= 1,
                f"Order_{o}_delay_in_{t}",
                )

# The problem data is written to an .lp file
prob.writeLP("nxp.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# # Each of the variables>0 is printed
# for v in prob.variables():
#     if (v.varValue>0):
#         print(v.name, "=", v.varValue)

#Each variable printed
for v in sorted(prob.variables(), key=lambda x: x.name):
    if v.varValue > 0:
        print(v.name, "=", v.varValue)

# n variables
print("# variables = ", len(prob.variables()))
# The optimised objective function value is printed to the screen
print("# constraints = ", len(prob.constraints))
# The optimised objective function value is printed to the screen
print("Total Cost = ", value(prob.objective))


#extract info
import pandas as pd


# Collect the variables and their values in a dictionary
all_variables = {v.name: v.varValue for v in prob.variables()}

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(list(all_variables.items()), columns=['var_name', 'var_value'])

#Create VarTypes
# Define a dict for mapping prefixes to their respective VarType values
prefix_to_var_type = {
    'order_delay': 'Order_delay',
    'starting_inventory': 'starting_inventory',
    'order_fulfillment': 'order_fulfillment',
    'resource_production': 'resource_production'
}

# Use a lambda function to apply the mapping based on the var_name prefix
df['VarType'] = df['var_name'].apply(lambda x: next((var_type for prefix, var_type in prefix_to_var_type.items() if x.startswith(prefix)), None))

summary_df=pd.DataFrame({
    'name':['Total_cost','Total_delay_cost','Production_cost','n_vars','n_constraints'],
    'value':[value(prob.objective),
             df[(df.VarType=='Order_delay')].var_value.sum()*unit_delay_cost,
             value(prob.objective)-df[(df.VarType=='Order_delay')].var_value.sum()*unit_delay_cost,
             len(prob.variables()),
             len(prob.constraints)]
    })

df.to_csv('test_variables.csv',mode='w',header=True,index=False)
summary_df.to_csv('test_summary.csv',mode='w',header=True,index=False)
