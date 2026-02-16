import streamlit as st
from typing import List, Dict, Optional

# Initialize session state
def init_session_state():
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "search_term" not in st.session_state:
        st.session_state.search_term = ""
    if "category_filter" not in st.session_state:
        st.session_state.category_filter = "All"

# Product catalog
PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics"},
    {"id": 2, "name": "Smartphone", "price": 699.99, "category": "Electronics"},
    {"id": 3, "name": "Headphones", "price": 149.99, "category": "Electronics"},
    {"id": 4, "name": "T-Shirt", "price": 19.99, "category": "Clothing"},
    {"id": 5, "name": "Jeans", "price": 49.99, "category": "Clothing"},
    {"id": 6, "name": "Coffee Mug", "price": 9.99, "category": "Home"},
]

# Helper functions
def format_currency(amount: float) -> str:
    return f"${amount:.2f}"

def get_unique_categories() -> List[str]:
    categories = {"All"}
    for product in PRODUCTS:
        categories.add(product["category"])
    return sorted(categories)

def filter_products(search_term: str, category_filter: str) -> List[Dict]:
    filtered = PRODUCTS
    if search_term:
        filtered = [p for p in filtered if search_term.lower() in p["name"].lower()]
    if category_filter != "All":
        filtered = [p for p in filtered if p["category"] == category_filter]
    return filtered

# Cart management
def add_to_cart(product_id: int, quantity: int = 1) -> None:
    if product_id not in st.session_state.cart:
        st.session_state.cart[product_id] = 0
    st.session_state.cart[product_id] += quantity

def update_quantity(product_id: int, quantity: int) -> bool:
    if quantity < 0:
        return False
    if product_id in st.session_state.cart:
        if quantity == 0:
            del st.session_state.cart[product_id]
        else:
            st.session_state.cart[product_id] = quantity
    return True

def remove_from_cart(product_id: int) -> None:
    if product_id in st.session_state.cart:
        del st.session_state.cart[product_id]

def clear_cart() -> None:
    st.session_state.cart = {}

# UI components
def display_products(filtered_products: List[Dict]) -> None:
    for product in filtered_products:
        cols = st.columns([3, 1, 1])
        with cols[0]:
            st.write(f"**{product['name']}** - {format_currency(product['price'])}")
        with cols[1]:
            quantity = st.number_input("Qty", min_value=1, max_value=10, key=f"qty_{product['id']}")
        with cols[2]:
            if st.button("Add", key=f"add_{product['id']}"):
                add_to_cart(product['id'], quantity)
                st.rerun()

def display_cart() -> None:
    if not st.session_state.cart:
        st.info("Your cart is empty")
        return

    st.subheader("Your Cart")
    total = 0.0

    for product_id, quantity in st.session_state.cart.items():
        product = next(p for p in PRODUCTS if p["id"] == product_id)
        subtotal = product["price"] * quantity
        total += subtotal

        cols = st.columns([2, 1, 1, 1, 1])
        with cols[0]:
            st.write(product["name"])
        with cols[1]:
            st.write(format_currency(product["price"]))
        with cols[2]:
            new_qty = st.number_input("Qty", min_value=0, max_value=10, value=quantity, key=f"cart_qty_{product_id}")
            if new_qty != quantity:
                if update_quantity(product_id, new_qty):
                    st.rerun()
        with cols[3]:
            st.write(format_currency(subtotal))
        with cols[4]:
            if st.button("Remove", key=f"remove_{product_id}"):
                remove_from_cart(product_id)
                st.rerun()

    st.write(f"**Total: {format_currency(total)}**")

    if st.button("Checkout"):
        st.session_state.order_summary = {
            "items": [{"name": p["name"], "price": p["price"], "quantity": q} for p_id, q in st.session_state.cart.items() for p in PRODUCTS if p["id"] == p_id],
            "total": total
        }
        st.rerun()

def display_checkout_modal() -> None:
    if "order_summary" in st.session_state:
        with st.form("checkout_form"):
            st.write("### Order Summary")
            for item in st.session_state.order_summary["items"]:
                st.write(f"{item['name']} x {item['quantity']} - {format_currency(item['price'] * item['quantity'])}")
            st.write(f"**Total: {format_currency(st.session_state.order_summary['total'])}**")

            if st.form_submit_button("Confirm Order"):
                clear_cart()
                st.success("Order placed successfully!")
                del st.session_state.order_summary
                st.rerun()

# Main app
def main():
    init_session_state()

    st.title("Shopping Cart")

    # Product browsing
    st.header("Products")
    cols = st.columns([2, 1])
    with cols[0]:
        st.session_state.search_term = st.text_input("Search products", value=st.session_state.search_term)
    with cols[1]:
        categories = get_unique_categories()
        st.session_state.category_filter = st.selectbox("Category", categories, index=list(categories).index(st.session_state.category_filter))

    filtered_products = filter_products(st.session_state.search_term, st.session_state.category_filter)
    display_products(filtered_products)

    # Cart display
    st.sidebar.header("Cart")
    display_cart()
    display_checkout_modal()

if __name__ == "__main__":
    main()

