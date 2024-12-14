from pulp import LpProblem, LpVariable,lpSum
from subpages.data_class_script_v2 import Order
def add_objective_terms_v2(model: LpProblem, order_list: list[Order],y_f:list,
                           multiplier: float,criticality:list[float],time_ids_f:list[int]):
    new_term = [
        multiplier * (t - o.deadline) ** 2 * criticality[o.order_id] * y_f[o.order_id][t] * o.product[o.product_id]
        for o in order_list for t in time_ids_f if t > o.deadline]
    model_copy = model.copy()

    model_copy.setObjective(lpSum(model_copy.objective + new_term))
    return model_copy

def check_delayed_orders(f_orders:list[Order], f_y:LpVariable, f_time_ids: list[int]):
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
                          f'totoal_delay:{total_delayed_units}')
                    delayed_orders.append(o.order_id)
    return sorted(set(delayed_orders)), total_delayed_units

