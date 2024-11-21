from dataclasses import dataclass, field
from typing import Dict, Optional
from collections import defaultdict
import random

@dataclass(frozen=True)
class Resource:
    resource_id:int
    resource_capacity:int
    name: str

    def __hash__(self):
        return hash(self.name)
    def __str__(self):
        return f'id:{self.resource_id},name:{self.name}'

@dataclass(frozen=True)
class Product:
    product_id:int
    name: str
    resource_usage: dict = field(default_factory=lambda: defaultdict(int))

    def __hash__(self):
        return hash(self.name)

@dataclass
class Order:
    order_id:int
    product_id:int
    customer_name: str
    deadline: int
    _product: Dict[Product, int] = field(default_factory=lambda: defaultdict(int))  # Product instances as keys
    product: Dict[int, int] = field(init=False)  # Product IDs as keys

    def __post_init__(self):
        """Initialize 'product' dict based on '_product'."""
        # Create a product_id-based dict from the _product dict
        self.product = defaultdict(int, {product.product_id: amount for product, amount in self._product.items()})
    #
    # @property
    # def total_resource_usage(self) -> Dict[Resource, int]:
    #     """Calculate total resource usage across all products in the order."""
    #     total_usage = defaultdict(int)
    #     for product, amount in self._product.items():
    #         for resource_id, usage_per_product in product.resource_usage.items():
    #             total_usage[resource_id] += usage_per_product * amount
    #     return total_usage


@dataclass(frozen=True)
class Customer:
    customer_id: int
    name: str

    def __hash__(self):
        return hash(self.name)

def generate_resources(n_resources,resource_capacity=100):
    resources=[Resource(name=f"resource_{i}",resource_id=i,resource_capacity=resource_capacity) for i in range(n_resources)]
    return resources

def generate_customers(n_customers):
    customers=[Customer(name=f"customer{i}",customer_id=i) for i in range(n_customers)]
    return customers
#
# def generate_products(n_products,resources,min_resource_needed=0,max_resource_needed=20):
#     products=[]
#     for i in range(n_products):
#         # Randomly assign some resources to the product
#         random_resources = random.sample(resources, random.randint(a=1, b=len(resources)))
#         random_resources_dict = {resource.resource_id: random.randint(min_resource_needed, max_resource_needed) for resource in random_resources}
#
#         products.append(
#             Product(name=f"product_{i}",
#                     product_id=i,
#                     resource_usage=defaultdict(int, random_resources_dict)
#                     )
#             )
#     return products

def generate_products():
    products=[]
    products.append(Product(name=f"product_0",product_id=0,resource_usage=defaultdict(lambda: 99999, {0:1})))
    products.append(Product(name=f"product_1",product_id=1,resource_usage=defaultdict(lambda: 99999, {1:1})))
    products.append(Product(name=f"product_2",product_id=2,resource_usage=defaultdict(lambda: 99999, {0:1,1:1})))
    return products

def generate_orders(n_orders,products,customers,time_periods,min_product_type=1,max_product_type=1,min_product_amt=10,max_product_amt=20):
    orders=[]
    for i in range(n_orders):
        # Randomly assign some resources to order
        random_products = random.sample(products, random.randint(a=min_product_type, b=max_product_type))
        random_products_dict = {product: random.randint(min_product_amt, max_product_amt) for product in random_products}

        orders.append(
            Order(order_id=i,
                  customer_name=random.choice(customers).name,
                  product_id=random_products[0].product_id,
                  deadline=random.choice(time_periods),
                  _product=defaultdict(int, random_products_dict)
            ))
    return orders


def determine_total_quantity_per_product(orders_f,products_f):
    total_quantity_per_product = defaultdict(lambda: 0)
    for o in orders_f:
        for p in products_f:
            if o.product[p.product_id] > 0.001:
                # print(f'id:{o.order_id},deadline:{o.deadline},product:{o.product}, q:{o.product[p]}')
                total_quantity_per_product[p.product_id] += o.product[p.product_id]
    return dict(total_quantity_per_product)

def retrieve_fulfill_times(orders_tmp:list[Order],y_vars:list,time_periods:list[int]):
    for o in orders_tmp:
        o.delay_status='on_time'
        for t in sorted(time_periods, reverse=True):
            if y_vars[o.order_id][t].varValue > 0:
                o.fulfilled = t
                if t>o.deadline:
                    o.delay_status = 'delayed'
                    o.delay_duration=t-o.deadline
                break  # Move to the next 'o' immediately after satisfying the condition
    return orders_tmp

def print_orders(orders):
    for o in orders:
        print(f'id:{o.order_id}, t:{o.deadline}, '
              f'{o.customer_name}, '
              f'product(id-qty):({o.product_id}-{o.product[o.product_id]})'
              )
