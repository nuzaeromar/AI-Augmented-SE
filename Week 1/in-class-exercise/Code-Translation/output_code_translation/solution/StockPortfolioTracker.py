<<<<<<< Updated upstream
class StockPortfolioTracker:
    def __init__(self, cash_balance):
        self.portfolio = []
        self.cash_balance = cash_balance

    def add_stock(self, stock):
        for pf in self.portfolio:
            if pf['name'] == stock['name']:
                pf['quantity'] += stock['quantity']
                return
        self.portfolio.append(stock)

    def remove_stock(self, stock):
        for i, pf in enumerate(self.portfolio):
            if pf['name'] == stock['name'] and pf['quantity'] >= stock['quantity']:
                pf['quantity'] -= stock['quantity']
                if pf['quantity'] == 0:
=======
class Stock:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    @staticmethod
    def from_input(data):
        if isinstance(data, Stock):
            return data
        if isinstance(data, dict):
            return Stock(
                name=data.get("name", ""),
                price=float(data.get("price", 0)),
                quantity=int(data.get("quantity", 0)),
            )
        raise TypeError("Unsupported stock representation")

    def __eq__(self, other):
        if isinstance(other, Stock):
            return (
                self.name == other.name
                and self.price == other.price
                and self.quantity == other.quantity
            )
        if isinstance(other, dict):
            return (
                self.name == other.get("name")
                and self.price == float(other.get("price", 0))
                and self.quantity == int(other.get("quantity", 0))
            )
        return False

    def to_dict(self):
        return {"name": self.name, "price": self.price, "quantity": self.quantity}


class StockSummary:
    def __init__(self, name: str, value: float):
        self.name = name
        self.value = value

    def __eq__(self, other):
        if isinstance(other, StockSummary):
            return self.name == other.name and self.value == other.value
        if isinstance(other, dict):
            return self.name == other.get("name") and self.value == other.get("value")
        return False

    def to_dict(self):
        return {"name": self.name, "value": self.value}


class StockPortfolioTracker:
    def __init__(self, cash_balance: float):
        self.cash_balance = float(cash_balance)
        self.portfolio = []  # list of Stock objects

    def _normalize(self, stock):
        """Accept dict or Stock and return a Stock instance."""
        return Stock.from_input(stock)

    def add_stock(self, stock):
        stk = self._normalize(stock)
        for existing in self.portfolio:
            if existing.name == stk.name:
                existing.quantity += stk.quantity
                return
        self.portfolio.append(stk)

    def remove_stock(self, stock) -> bool:
        stk = self._normalize(stock)
        for i, existing in enumerate(self.portfolio):
            if (
                existing.name == stk.name
                and existing.quantity >= stk.quantity
            ):
                existing.quantity -= stk.quantity
                if existing.quantity == 0:
>>>>>>> Stashed changes
                    self.portfolio.pop(i)
                return True
        return False

<<<<<<< Updated upstream
    def buy_stock(self, stock):
        if stock['price'] * stock['quantity'] > self.cash_balance:
            return False
        else:
            self.add_stock(stock)
            self.cash_balance -= stock['price'] * stock['quantity']
            return True

    def sell_stock(self, stock):
        if not self.remove_stock(stock):
            return False
        self.cash_balance += stock['price'] * stock['quantity']
        return True

    def calculate_portfolio_value(self):
        total_value = self.cash_balance
        for stock in self.portfolio:
            total_value += stock['price'] * stock['quantity']
        return total_value

    def get_portfolio_summary(self):
        summary = []
        for stock in self.portfolio:
            summary.append({'name': stock['name'], 'value': self.get_stock_value(stock)})
        return (self.calculate_portfolio_value(), summary)

    def get_stock_value(self, stock):
        return stock['price'] * stock['quantity']

    def get_portfolio(self):
=======
    def buy_stock(self, stock) -> bool:
        stk = self._normalize(stock)
        total_price = stk.price * stk.quantity
        if total_price > self.cash_balance:
            return False
        self.add_stock(stk)
        self.cash_balance -= total_price
        return True

    def sell_stock(self, stock) -> bool:
        stk = self._normalize(stock)
        if not self.remove_stock(stk):
            return False
        self.cash_balance += stk.price * stk.quantity
        return True

    def calculate_portfolio_value(self) -> float:
        total = self.cash_balance
        for s in self.portfolio:
            total += s.price * s.quantity
        return total

    def get_portfolio_summary(self):
        summaries = [
            StockSummary(s.name, self.get_stock_value(s)) for s in self.portfolio
        ]
        # Return as (total_value, list_of_summaries)
        return (self.calculate_portfolio_value(), summaries)

    def get_stock_value(self, stock) -> float:
        stk = self._normalize(stock)
        return stk.price * stk.quantity

    def get_portfolio(self):
        # Return list of Stock objects (tests may also accept dicts)
>>>>>>> Stashed changes
        return self.portfolio

    def get_cash_balance(self):
        return self.cash_balance

<<<<<<< Updated upstream
    def set_portfolio(self, p):
        self.portfolio = p
=======
    def set_portfolio(self, portfolio):
        normalized = [self._normalize(s) for s in portfolio]
        self.portfolio = normalized
>>>>>>> Stashed changes
