import streamlit as st
from typing import Dict, List, Optional, Tuple
import uuid

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'search_term' not in st.session_state:
    st.session_state.search_term = ""
if 'category_filter' not in st.session_state:
    st.session_state.category_filter = "All"

# Product catalog
PRODUCTS = [
    {"id": "p1", "name": "Laptop", "price": 999.99, "category": "Electronics"},
    {"id": "p2", "name": "Smartphone", "price": 699.99, "category": "Electronics"},
    {"id": "p3", "name": "Headphones", "price": 149.99, "category": "Electronics"},
    {"id": "p4", "name": "T-Shirt", "price": 19.99, "category": "Clothing"},
    {"id": "p5", "name": "Jeans", "price": 49.99, "category": "Clothing"},
    {"id": "p6", "name": "Sneakers", "price": 79.99, "category": "Clothing"},
]

# Helper function for currency formatting
def format_price(price: float) -> str:
    return f"${price:.2f}"

# Product browsing UI
def display_products():
    st.header("Product Catalog")

    # Search and filter
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.search_term = st.text_input("Search products", value=st.session_state.search_term)
    with col2:
        categories = ["All"] + sorted({p["category"] for p in PRODUCTS})
        st.session_state.category_filter = st.selectbox("Filter by category", categories, index=0)

    # Filter products
    filtered_products = [
        p for p in PRODUCTS
        if (st.session_state.search_term.lower() in p["name"].lower() or not st.session_state.search_term)
        and (st.session_state.category_filter == "All" or p["category"] == st.session_state.category_filter)
    ]

    # Display products
    if not filtered_products:
        st.warning("No products found matching your criteria.")
        return

    st.table({
        "Product": [p["name"] for p in filtered_products],
        "Price": [format_price(p["price"]) for p in filtered_products],
        "Category": [p["category"] for p in filtered_products],
        "Add to Cart": ["➕" for _ in filtered_products]
    })

    # Add to cart buttons
    for i, product in enumerate(filtered_products):
        if st.button(f"Add {product['name']} to Cart", key=f"add_{product['id']}"):
            if product['id'] in st.session_state.cart:
                st.session_state.cart[product['id']]['quantity'] += 1
            else:
                st.session_state.cart[product['id']] = {
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': 1
                }
            st.success(f"{product['name']} added to cart!")

# Cart management
def display_cart():
    st.header("Shopping Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty.")
        return

    # Display cart items
    cart_items = []
    for item_id, item in st.session_state.cart.items():
        cart_items.append({
            "Product": item['name'],
            "Price": format_price(item['price']),
            "Quantity": st.number_input(
                f"Qty for {item['name']}",
                min_value=1,
                value=item['quantity'],
                key=f"qty_{item_id}",
                on_change=lambda: update_quantity(item_id)
            ),
            "Subtotal": format_price(item['price'] * item['quantity']),
            "Remove": st.button(f"Remove {item['name']}", key=f"remove_{item_id}")
        })

        if cart_items[-1]["Remove"]:
            del st.session_state.cart[item_id]
            st.rerun()

    st.table(cart_items)

    # Cart totals
    total = sum(item['price'] * item['quantity'] for item in st.session_state.cart.values())
    st.write(f"**Total:** {format_price(total)}")

    # Cart actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Cart"):
            st.session_state.cart = {}
            st.rerun()
    with col2:
        if st.button("Checkout"):
            show_checkout_modal(total)

def update_quantity(item_id: str):
    try:
        new_qty = st.session_state[f"qty_{item_id}"]
        if new_qty < 1:
            st.error("Quantity must be at least 1")
            st.session_state[f"qty_{item_id}"] = st.session_state.cart[item_id]['quantity']
        else:
            st.session_state.cart[item_id]['quantity'] = new_qty
    except Exception as e:
        st.error(f"Error updating quantity: {e}")

def show_checkout_modal(total: float):
    with st.form("checkout_form"):
        st.write("### Order Summary")
        for item_id, item in st.session_state.cart.items():
            st.write(f"- {item['name']} x {item['quantity']} = {format_price(item['price'] * item['quantity'])}")

        st.write(f"**Total:** {format_price(total)}")

        if st.form_submit_button("Confirm Order"):
            st.session_state.cart = {}
            st.success("Order placed successfully!")
            st.rerun()

# Main app
def main():
    st.title("Streamlit Shopping Cart")

    # Layout
    col1, col2 = st.columns([3, 1])
    with col1:
        display_products()
    with col2:
        display_cart()

    # Footer
    st.markdown("---")
    st.write("App Version: 1.0.0")

if __name__ == "__main__":
    main()

