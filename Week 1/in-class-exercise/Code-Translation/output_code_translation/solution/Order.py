class Order:
    def __init__(self):
<<<<<<< Updated upstream
        self.menu = []
        self.selected_dishes = []
        self.sales = {}

    def add_dish(self, dish):
        for menu_dish in self.menu:
            if dish['dish'] == menu_dish['dish']:
                if menu_dish['count'] < dish['count']:
                    return False
                else:
                    menu_dish['count'] -= dish['count']
                    break
        self.selected_dishes.append(dish)
        return True

    def calculate_total(self):
        total = 0
        for dish in self.selected_dishes:
            if dish['dish'] in self.sales:
                total += dish['price'] * dish['count'] * self.sales[dish['dish']]
        return total

    def checkout(self):
=======
        self.menu = []               # list of dishes (dicts or objects)
        self.selected_dishes = []   # list of dishes added to order
        self.sales = {}              # mapping dish name -> multiplier (float)

    def _get_attr(self, obj, attr):
        if isinstance(obj, dict):
            return obj.get(attr)
        return getattr(obj, attr, None)

    def _set_attr(self, obj, attr, value):
        if isinstance(obj, dict):
            obj[attr] = value
        else:
            setattr(obj, attr, value)

    def add_dish(self, dish):
        """
        Attempt to add a dish to the order.

        Returns:
            bool: True if the dish was successfully added, False otherwise.
        """
        dish_name = self._get_attr(dish, "dish")
        dish_count = self._get_attr(dish, "count")

        for menu_dish in self.menu:
            if self._get_attr(menu_dish, "dish") == dish_name:
                available = self._get_attr(menu_dish, "count")
                if available < dish_count:
                    return False
                # reduce the available count in the menu
                self._set_attr(menu_dish, "count", available - dish_count)
                break

        # store the requested dish in the selected list
        self.selected_dishes.append(dish)
        return True

    def calculate_total(self) -> float:
        """
        Calculate total price for currently selected dishes, applying sales multipliers.

        Returns:
            float: The total amount.
        """
        total = 0.0
        for dish in self.selected_dishes:
            name = self._get_attr(dish, "dish")
            price = self._get_attr(dish, "price")
            count = self._get_attr(dish, "count")
            multiplier = self.sales.get(name)
            if multiplier is not None:
                total += price * count * multiplier
        return total

    def checkout(self) -> float:
        """
        Finalize the order: return total and clear selected dishes.

        Returns:
            float: Total amount for the order, or 0 if no dishes selected.
        """
>>>>>>> Stashed changes
        if not self.selected_dishes:
            return 0
        total = self.calculate_total()
        self.selected_dishes.clear()
        return total
