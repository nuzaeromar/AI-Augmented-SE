import streamlit as st
from utils import Product, add_to_cart, remove_from_cart, clear_cart, calculate_total

# Sample product data
PRODUCTS = [
    Product("Laptop", 999.99, "High-performance laptop"),
    Product("Smartphone", 699.99, "Latest smartphone model"),
    Product("Headphones", 149.99, "Noise-cancelling headphones"),
    Product("Keyboard", 49.99, "Mechanical gaming keyboard"),
    Product("Mouse", 29.99, "Wireless gaming mouse"),
]

def main():
    st.title("Shopping Cart")

    # Initialize session state for cart
    if "cart" not in st.session_state:
        st.session_state.cart = []

    # Product listing
    st.header("Products")
    for product in PRODUCTS:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{product.name}** - ${product.price:.2f}")
            st.caption(product.description)
        with col2:
            if st.button("Add to Cart", key=f"add_{product.name}"):
                add_to_cart(st.session_state.cart, product)
        with col3:
            st.write(f"In Cart: {st.session_state.cart.count(product)}")

    # Cart display
    st.header("Shopping Cart")
    if not st.session_state.cart:
        st.write("Your cart is empty.")
    else:
        for item in st.session_state.cart:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item.name}** - ${item.price:.2f}")
            with col2:
                if st.button("Remove", key=f"remove_{item.name}_{st.session_state.cart.index(item)}"):
                    remove_from_cart(st.session_state.cart, item)
            with col3:
                st.write(f"Qty: {st.session_state.cart.count(item)}")

        st.write(f"**Total: ${calculate_total(st.session_state.cart):.2f}**")

        if st.button("Checkout"):
            st.success("Order placed successfully!")
            clear_cart(st.session_state.cart)

if __name__ == "__main__":
    main()
