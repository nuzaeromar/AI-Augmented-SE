import json
import os
from typing import Any, Dict, List, Optional, Union


class TextFileProcessor:
    def __init__(self, filename):
        self.filename = filename

<<<<<<< Updated upstream
    def read_file_as_json(self):
        with open(self.filename, 'r') as file:
            return json.load(file)

    def read_file(self):
        with open(self.filename, 'r') as file:
            return file.read()

    def write_file(self, content):
        with open(self.filename, 'w') as file:
            file.write(content)
=======
    def read_file_as_json(self) -> Any:
        with open(self.filename_, "r", encoding="utf-8") as f:
            return json.load(f)

    def read_file(self) -> str:
        with open(self.filename_, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, content: str) -> None:
        with open(self.filename_, "w", encoding="utf-8") as f:
            f.write(content)
>>>>>>> Stashed changes

    def process_file(self):
        content = self.read_file()
<<<<<<< Updated upstream
        result = ''.join([c for c in content if c.isalpha()])
=======
        result = "".join(c for c in content if c.isalpha())
>>>>>>> Stashed changes
        self.write_file(result)
        return result


class JSONProcessor:
    def read_json(self, path: str, output: Optional[Dict] = None) -> Optional[Dict]:
        """Read a JSON file.

        If `output` is provided, it is cleared and updated with the parsed data,
        and the method returns None. Otherwise, the parsed dictionary is returned.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if output is not None:
            if not isinstance(output, dict):
                raise TypeError("output must be a dict if provided")
            output.clear()
            output.update(data)
            return None
        return data


class StockPortfolioTracker:
    def __init__(self, portfolio: Optional[List[Dict]] = None):
        self._portfolio = portfolio if portfolio is not None else []

    @property
    def portfolio(self) -> List[Dict]:
        return self._portfolio

    @portfolio.setter
    def portfolio(self, value: List[Dict]) -> None:
        if not isinstance(value, list):
            raise TypeError("portfolio must be a list")
        self._portfolio = value


class VendingMachine:
    def __init__(self):
        self.inventory: Dict[str, Dict[str, Union[float, int]]] = {}
        self.balance: float = 0.0

    def insert_coin(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Inserted amount must be positive")
        self.balance += amount

    def add_item(self, name: str, price: float, quantity: int) -> None:
        if quantity < 0 or price < 0:
            raise ValueError("Price and quantity must be non‑negative")
        self.inventory[name] = {"price": price, "quantity": quantity}

    def purchase_item(self, name: str) -> bool:
        """Attempt to purchase one unit of `name`.

        Returns True if the purchase succeeded, otherwise False.
        """
        if name not in self.inventory:
            return False
        item = self.inventory[name]
        if item["quantity"] <= 0:
            return False
        if self.balance < item["price"]:
            return False

        # Perform transaction
        self.balance -= item["price"]
        item["quantity"] -= 1
        return True

    def restock_item(self, name: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Restock quantity must be positive")
        if name not in self.inventory:
            raise KeyError(f"Item '{name}' not found in inventory")
        self.inventory[name]["quantity"] += quantity


class SQLQueryBuilder:
    @staticmethod
    def select(table: str,
               columns: Optional[List[str]] = None,
               where: Optional[Dict[str, Any]] = None) -> str:
        cols_part = "*"
        if columns:
            cols_part = ", ".join(columns)
        query = f"SELECT {cols_part} FROM {table}"
        if where:
            conditions = " AND ".join(
                f"{k} = {SQLQueryBuilder._format_value(v)}" for k, v in where.items()
            )
            query += f" WHERE {conditions}"
        query += ";"
        return query

    @staticmethod
    def insert(table: str, data: Dict[str, Any]) -> str:
        columns = ", ".join(data.keys())
        values = ", ".join(SQLQueryBuilder._format_value(v) for v in data.values())
        return f"INSERT INTO {table} ({columns}) VALUES ({values});"

    @staticmethod
    def update(table: str, data: Dict[str, Any], where: Dict[str, Any]) -> str:
        set_clause = ", ".join(
            f"{k} = {SQLQueryBuilder._format_value(v)}" for k, v in data.items()
        )
        where_clause = " AND ".join(
            f"{k} = {SQLQueryBuilder._format_value(v)}" for k, v in where.items()
        )
        return f"UPDATE {table} SET {set_clause} WHERE {where_clause};"

    @staticmethod
    def delete(table: str, where: Optional[Dict[str, Any]] = None) -> str:
        query = f"DELETE FROM {table}"
        if where:
            conditions = " AND ".join(
                f"{k} = {SQLQueryBuilder._format_value(v)}" for k, v in where.items()
            )
            query += f" WHERE {conditions}"
        query += ";"
        return query

    @staticmethod
    def _format_value(value: Any) -> str:
        if isinstance(value, str):
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        return str(value)
