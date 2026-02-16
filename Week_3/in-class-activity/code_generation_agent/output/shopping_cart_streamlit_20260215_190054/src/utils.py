from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    description: str

def add_to_cart(cart, product):
    cart.append(product)

def remove_from_cart(cart, product):
    if product in cart:
        cart.remove(product)

def clear_cart(cart):
    cart.clear()

def calculate_total(cart):
    return sum(item.price for item in cart)
