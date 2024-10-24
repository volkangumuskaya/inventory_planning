from dataclasses import dataclass, field
from typing import Dict, Optional
from collections import defaultdict
import random

@dataclass(frozen=True)
class Resource:
    resource_id:int
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
    customer_name: str
    deadline: int
    _product: Dict[Product, int] = field(default_factory=lambda: defaultdict(int))  # Product instances as keys
    product: Dict[int, int] = field(init=False)  # Product IDs as keys

    def __post_init__(self):
        """Initialize 'product' dict based on '_product'."""
        # Create a product_id-based dict from the _product dict
        self.product = defaultdict(int, {product.product_id: amount for product, amount in self._product.items()})


    @property
    def total_resource_usage(self) -> Dict[Resource, int]:
        """Calculate total resource usage across all products in the order."""
        total_usage = defaultdict(int)
        for product, amount in self._product.items():
            for resource_id, usage_per_product in product.resource_usage.items():
                total_usage[resource_id] += usage_per_product * amount
        return total_usage


@dataclass(frozen=True)
class Customer:
    customer_id: int
    name: str

    def __hash__(self):
        return hash(self.name)

def generate_resources(n_resources):
    resources=[Resource(name=f"resource_{i}",resource_id=i) for i in range(n_resources)]
    return resources

def generate_customers(n_customers):
    customers=[Customer(name=f"customer{i}",customer_id=i) for i in range(n_customers)]
    return customers

def generate_products(n_products,resources,min_resource_needed=0,max_resource_needed=20):
    products=[]
    for i in range(n_products):
        # Randomly assign some resources to the product
        random_resources = random.sample(resources, random.randint(a=1, b=len(resources)))
        random_resources_dict = {resource.resource_id: random.randint(min_resource_needed, max_resource_needed) for resource in random_resources}

        products.append(
            Product(name=f"product_{i}",
                    product_id=i,
                    resource_usage=defaultdict(int, random_resources_dict)
                    )
            )
    return products

def generate_orders(n_orders,products,customers,time_periods,min_product_type=2,max_product_type=4,min_product_amt=10,max_product_amt=20):
    orders=[]
    for i in range(n_orders):
        # Randomly assign some resources to order
        random_products = random.sample(products, random.randint(a=min_product_type, b=max_product_type))
        random_products_dict = {product: random.randint(min_product_amt, max_product_amt) for product in random_products}

        orders.append(
            Order(order_id=i,
                  customer_name=random.choice(customers),
                  deadline=random.choice(time_periods),
                  _product=defaultdict(int, random_products_dict)
            ))
    return orders


