import json
import os
<<<<<<< Updated upstream

class JSONProcessor:

    def read_json(self, file_path, output):
        try:
            with open(file_path, 'r') as file:
                output = json.load(file)
                if output is None:
                    return -1
        except:
            return -1

        return 1

    def write_json(self, data, file_path):
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except:
=======
from typing import Any, Dict, List, Optional, Union


class JSONProcessor:
    """
    Provides basic JSON file operations analogous to the original C++ implementation.
    """

    def read_json(self, file_path: str, output: Optional[Dict] = None) -> Union[int, Dict, None]:
        """
        Reads a JSON file.

        If `output` is provided, it will be populated with the parsed JSON content
        and the method returns a status code:
            1  – success
            0  – file could not be opened
           -1  – parsing error or JSON is null

        If `output` is None, the parsed JSON object (a dict) is returned on success,
        otherwise the same status codes are returned.
        """
        if not os.path.exists(file_path):
            return 0

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return -1

        if data is None:
            return -1

        if output is not None:
            if not isinstance(output, dict):
                raise TypeError("output must be a dict when provided")
            output.clear()
            if isinstance(data, dict):
                output.update(data)
            else:
                # If the JSON root is not an object, store it under a generic key.
                output["value"] = data
            return 1
        else:
            return data

    def write_json(self, data: Any, file_path: str) -> int:
        """
        Writes `data` to a JSON file with 4‑space indentation.

        Returns:
            1  – success
           -1  – failure to open or write the file
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception:
>>>>>>> Stashed changes
            return -1

        return 1

<<<<<<< Updated upstream
    def process_json(self, file_path, remove_key):
        data = None
        result = self.read_json(file_path, data)
=======
    def process_json(self, file_path: str, remove_key: str) -> int:
        """
        Reads a JSON file, removes `remove_key` if present, and writes the result back.
>>>>>>> Stashed changes

        Returns:
            1  – key removed and file rewritten successfully
            0  – file could not be opened, key not present, or read error
           -1  – write error
        """
        result = self.read_json(file_path)
        if isinstance(result, int):
            # read_json returned a status code (0 or -1)
            return 0
        data = result
        if not isinstance(data, dict):
            return 0
        if remove_key in data:
            del data[remove_key]
            write_status = self.write_json(data, file_path)
            return write_status
        return 0


class StockPortfolioTracker:
    """
    Simple portfolio tracker where `portfolio` is a mutable list of holdings.
    Each holding is expected to be a dict with keys: "name", "price", "quantity".
    """

    def __init__(self):
        self.portfolio: List[Dict] = []

    def total_value(self) -> float:
        """Calculate the total market value of the portfolio."""
        total = 0.0
        for holding in self.portfolio:
            try:
                price = float(holding.get("price", 0))
                qty = float(holding.get("quantity", 0))
                total += price * qty
            except (TypeError, ValueError):
                continue
        return total


class VendingMachine:
    """
    Represents a vending machine with an inventory and a monetary balance.
    """

    def __init__(self):
        # inventory format: {"ItemName": {"price": float, "quantity": int}}
        self.inventory: Dict[str, Dict[str, Union[float, int]]] = {}
        self.balance: float = 0.0

    # ----- monetary operations -----
    def insert_coin(self, amount: float) -> None:
        """Add money to the machine's balance."""
        if amount < 0:
            raise ValueError("Cannot insert a negative amount")
        self.balance += amount

    # ----- inventory management -----
    def add_item(self, name: str, price: float, quantity: int = 0) -> None:
        """Add a new item type or update an existing one."""
        if quantity < 0 or price < 0:
            raise ValueError("Price and quantity must be non‑negative")
        if name not in self.inventory:
            self.inventory[name] = {"price": price, "quantity": quantity}
        else:
            self.inventory[name]["price"] = price
            self.inventory[name]["quantity"] += quantity

    def restock_item(self, name: str, quantity: int) -> None:
        """Increase the quantity of an existing item."""
        if quantity < 0:
            raise ValueError("Quantity must be non‑negative")
        if name not in self.inventory:
            raise KeyError(f"Item '{name}' not found in inventory")
        self.inventory[name]["quantity"] += quantity

    def purchase_item(self, name: str, quantity: int = 1) -> bool:
        """
        Attempt to purchase `quantity` units of `name`.

        Returns True if the transaction succeeds, False otherwise.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if name not in self.inventory:
            return False

        item = self.inventory[name]
        total_price = item["price"] * quantity

        if item["quantity"] < quantity or self.balance < total_price:
            return False

        # Perform transaction
        item["quantity"] -= quantity
        self.balance -= total_price
        return True

    # ----- helper introspection -----
    def get_item_info(self, name: str) -> Optional[Dict[str, Union[float, int]]]:
        """Return a copy of the item description, or None if not found."""
        if name in self.inventory:
            return dict(self.inventory[name])
        return None


class SQLQueryBuilder:
    """
    Generates simple SQL statements from Python dictionaries.
    """

    @staticmethod
    def select(table: str,
               columns: Optional[List[str]] = None,
               where: Optional[Dict[str, Any]] = None) -> str:
        cols = "*"
        if columns:
            cols = ", ".join(columns)
        sql = f"SELECT {cols} FROM {table}"
        if where:
            conditions = []
            for k, v in where.items():
                val = f"'{v}'" if isinstance(v, str) else str(v)
                conditions.append(f"{k} = {val}")
            sql += " WHERE " + " AND ".join(conditions)
        return sql + ";"

    @staticmethod
    def insert(table: str, data: Dict[str, Any]) -> str:
        if not data:
            raise ValueError("Insert data cannot be empty")
        columns = list(data.keys())
        values = []
        for _, v in data.items():
            values.append(f"'{v}'" if isinstance(v, str) else str(v))
        cols_str = ", ".join(columns)
        vals_str = ", ".join(values)
        return f"INSERT INTO {table} ({cols_str}) VALUES ({vals_str});"

    @staticmethod
    def update(table: str,
               data: Dict[str, Any],
               where: Optional[Dict[str, Any]] = None) -> str:
        if not data:
            raise ValueError("Update data cannot be empty")
        set_parts = []
        for k, v in data.items():
            val = f"'{v}'" if isinstance(v, str) else str(v)
            set_parts.append(f"{k} = {val}")
        sql = f"UPDATE {table} SET " + ", ".join(set_parts)
        if where:
            conditions = []
            for k, v in where.items():
                val = f"'{v}'" if isinstance(v, str) else str(v)
                conditions.append(f"{k} = {val}")
            sql += " WHERE " + " AND ".join(conditions)
        return sql + ";"

    @staticmethod
    def delete(table: str, where: Optional[Dict[str, Any]] = None) -> str:
        sql = f"DELETE FROM {table}"
        if where:
            conditions = []
            for k, v in where.items():
                val = f"'{v}'" if isinstance(v, str) else str(v)
                conditions.append(f"{k} = {val}")
            sql += " WHERE " + " AND ".join(conditions)
        return sql + ";"
