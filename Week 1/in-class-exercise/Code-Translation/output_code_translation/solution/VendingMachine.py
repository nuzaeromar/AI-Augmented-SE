class VendingMachine:
    def __init__(self):
<<<<<<< Updated upstream
        self.balance_ = 0.0
        self.inventory_ = {}

    def add_item(self, item_name, price, quantity):
=======
        # public attributes
        self.inventory = {}          # {"ItemName": {"price": float, "quantity": int}}
        self.balance = 0.0

    # ----- core functionality -----
    def add_item(self, item_name, price, quantity):
        """
        Add a new item or restock an existing one.
        If the item already exists, restock_item handles the quantity increase.
        Otherwise, create a new entry with given price and quantity.
        """
>>>>>>> Stashed changes
        if not self.restock_item(item_name, quantity):
            # New item: store price and quantity
            self.inventory[item_name] = {
                "price": float(price),
                "quantity": int(quantity)
            }

    def insert_coin(self, amount):
<<<<<<< Updated upstream
        self.balance_ += amount
        return self.balance_

    def purchase_item(self, item_name):
        if item_name in self.inventory_:
            item = self.inventory_[item_name]
            if item["quantity"] > 0 and self.balance_ >= item["price"]:
                self.balance_ -= item["price"]
=======
        """Add amount to current balance and return the new balance."""
        self.balance += float(amount)
        return self.balance

    def purchase_item(self, item_name):
        """
        Attempt to purchase the given item.
        Returns the updated balance on success, otherwise returns False.
        """
        if item_name in self.inventory:
            item = self.inventory[item_name]
            if item["quantity"] > 0 and self.balance >= item["price"]:
                self.balance -= item["price"]
>>>>>>> Stashed changes
                item["quantity"] -= 1
                return self.balance
        return False

    def restock_item(self, item_name, quantity):
<<<<<<< Updated upstream
        if item_name in self.inventory_:
            self.inventory_[item_name]["quantity"] += float(quantity)
=======
        """
        Increase quantity of an existing item.
        Returns True if the item existed and was restocked, otherwise False.
        """
        if item_name in self.inventory:
            self.inventory[item_name]["quantity"] += int(quantity)
>>>>>>> Stashed changes
            return True
        return False

    def display_items(self):
<<<<<<< Updated upstream
        if not self.inventory_:
            return "false"

        items = []
        for item_name, item in self.inventory_.items():
            items.append(f"{item_name} - ${item['price']} [{item['quantity']}]")
        return "\n".join(items)

    def inventory(self):
        return self.inventory_

    def set_inventory(self, x):
        self.inventory_ = x

    def set_balance(self, y):
        self.balance_ = y
=======
        """
        Return a string listing all items, their price, and quantity.
        If inventory is empty, return the string "false".
        """
        if not self.inventory:
            return "false"

        lines = []
        # deterministic order for unit‑test stability
        for name in sorted(self.inventory.keys()):
            item = self.inventory[name]
            lines.append(f"{name} - ${item['price']} [{item['quantity']}]")
        result = "\n".join(lines)
        return result

    # ----- optional setters matching the original C++ interface -----
    def set_inventory(self, new_inventory):
        """Replace the entire inventory with the provided dictionary."""
        self.inventory = new_inventory

    def set_balance(self, new_balance):
        """Set the current balance to the provided value."""
        self.balance = float(new_balance)
>>>>>>> Stashed changes
