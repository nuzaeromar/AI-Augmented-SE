class ShoppingCart:
    def __init__(self):
<<<<<<< Updated upstream
        self.items = {}

    def add_item(self, item, price, quantity=1):
        self.items[item] = {'price': price, 'quantity': quantity}

    def remove_item(self, item, quantity=1):
        if item in self.items:
            self.items[item]['quantity'] -= quantity
            if self.items[item]['quantity'] <= 0:
                del self.items[item]

    def view_items(self):
        return self.items

    def total_price(self):
        total = 0.0
        for info in self.items.values():
            total += info['price'] * info['quantity']
=======
        # Internal storage: item -> {"price": float, "quantity": int}
        self._items: dict[str, dict] = {}

    def add_item(self, item: str, price: float, quantity: int = 1) -> None:
        """
        Add an item to the cart. If the item already exists, its price and
        quantity are overwritten (mirroring the original C++ behavior).
        """
        self._items[item] = {"price": price, "quantity": quantity}

    def remove_item(self, item: str, quantity: int = 1) -> None:
        """
        Decrease the quantity of *item* by *quantity*. If the resulting
        quantity is zero or negative, the item is removed from the cart.
        """
        if item in self._items:
            self._items[item]["quantity"] -= quantity
            if self._items[item]["quantity"] <= 0:
                del self._items[item]

    def view_items(self) -> dict:
        """
        Return a dictionary representation of the cart contents.
        Structure:
            {
                "item_name": {"price": <float>, "quantity": <int>},
                ...
            }
        """
        return self._items

    def total_price(self) -> float:
        """
        Compute the total price of all items in the cart.
        """
        total = 0.0
        for info in self._items.values():
            total += info["price"] * info["quantity"]
>>>>>>> Stashed changes
        return total
