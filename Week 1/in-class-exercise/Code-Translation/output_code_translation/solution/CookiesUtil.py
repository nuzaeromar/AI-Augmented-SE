import json
import os
<<<<<<< Updated upstream
=======
from typing import Any, Dict, List, Optional, Union

>>>>>>> Stashed changes

class CookiesUtil:
    def __init__(self, cookiesFile):
        self.cookies_file = cookiesFile
        self.cookies = {}

<<<<<<< Updated upstream
    def get_cookies(self, response):
        if "cookies" in response:
            self.cookies = response["cookies"]
        self._save_cookies()

    def load_cookies(self):
        cookiesData = {}
        if os.path.exists(self.cookies_file):
            try:
                with open(self.cookies_file, 'r') as file:
                    cookiesData = json.load(file)
            except Exception as e:
                print(f"Error reading JSON file: {e}")
        return cookiesData

    def _save_cookies(self):
        cookiesJson = self.cookies
        try:
            with open(self.cookies_file, 'w') as file:
                json.dump(cookiesJson, file, indent=4)
            return True
        except Exception as e:
            print(f"Error writing JSON file: {e}")
            return False

    def set_cookies(self, request):
        oss = []
        for key, value in self.cookies.items():
            if oss:
                oss.append("; ")
            oss.append(f"{key}={value}")
        request["cookies"] = "".join(oss)
=======
    def get_cookies(self, response: Union[Dict, Any]) -> None:
        """
        Extracts cookies from a JSON‑like response and saves them internally.
        If `response` contains a key named "cookies" it must be a mapping of
        string to string.
        """
        if isinstance(response, dict) and "cookies" in response:
            # Accept both dict and objects that behave like dicts
            self.cookies = dict(response["cookies"])
        else:
            # Try attribute access if a non‑dict object is given
            if hasattr(response, "contains") and response.contains("cookies"):
                self.cookies = dict(response["cookies"])
        self._save_cookies()

    def load_cookies(self) -> Dict[str, Any]:
        """
        Loads the cookies JSON file and returns its content as a dictionary.
        If the file does not exist or cannot be parsed, an empty dict is returned.
        """
        cookies_data: Dict[str, Any] = {}
        if not os.path.isfile(self.cookies_file):
            return cookies_data
        try:
            with open(self.cookies_file, "r", encoding="utf-8") as f:
                cookies_data = json.load(f)
        except Exception:
            # Silently ignore read errors – behaviour mirrors the C++ version
            pass
        return cookies_data

    def _save_cookies(self) -> bool:
        """
        Persists the current `self.cookies` dictionary to `self.cookies_file`
        in pretty‑printed JSON format. Returns True on success, False otherwise.
        """
        try:
            with open(self.cookies_file, "w", encoding="utf-8") as f:
                json.dump(self.cookies, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def set_cookies(self, request: Union[Dict, Any]) -> None:
        """
        Serialises stored cookies into a single header string of the form
        "key1=value1; key2=value2" and stores it under the key "cookies" in
        the given request mapping (dict‑like).
        """
        parts: List[str] = []
        for key, value in self.cookies.items():
            parts.append(f"{key}={value}")
        cookie_header = "; ".join(parts)
        if isinstance(request, dict):
            request["cookies"] = cookie_header
        else:
            setattr(request, "cookies", cookie_header)


class JSONProcessor:
    """
    Reads JSON files.  If `output` is supplied it is populated and the
    function returns None; otherwise the parsed JSON object is returned.
    """
    @staticmethod
    def read_json(path: str, output: Optional[Dict] = None) -> Optional[Dict]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
        if output is not None:
            output.clear()
            output.update(data)
            return None
        return data


class StockPortfolioTracker:
    """
    Tracks a list of holdings.  Each holding is a dict (or object) with at least
    the keys/attributes: "name", "price", "quantity".
    """
    def __init__(self):
        self.portfolio: List[Dict[str, Any]] = []

    def add_holding(self, holding: Union[Dict, Any]) -> None:
        """
        Adds a holding to the portfolio.  Accepts a dict or an object
        with the required attributes.
        """
        if isinstance(holding, dict):
            self.portfolio.append(holding)
        else:
            self.portfolio.append({
                "name": getattr(holding, "name", None),
                "price": getattr(holding, "price", None),
                "quantity": getattr(holding, "quantity", None),
            })

    def total_value(self) -> float:
        """Returns the total monetary value of the portfolio."""
        total = 0.0
        for h in self.portfolio:
            price = h.get("price", 0) if isinstance(h, dict) else getattr(h, "price", 0)
            qty = h.get("quantity", 0) if isinstance(h, dict) else getattr(h, "quantity", 0)
            try:
                total += float(price) * float(qty)
            except Exception:
                continue
        return total


class VendingMachine:
    """
    Simple vending‑machine simulation.
    - `inventory` is a public dict mapping item name → {"price": float, "quantity": int}
    - `balance` is a public float representing money inserted by the user.
    """
    def __init__(self):
        self.inventory: Dict[str, Dict[str, Any]] = {}
        self.balance: float = 0.0

    def add_item(self, name: str, price: float, quantity: int) -> None:
        """Adds a new item or updates an existing one."""
        if name in self.inventory:
            self.inventory[name]["price"] = price
            self.inventory[name]["quantity"] += quantity
        else:
            self.inventory[name] = {"price": price, "quantity": quantity}

    def insert_coin(self, amount: float) -> None:
        """Adds money to the current balance."""
        self.balance += float(amount)

    def purchase_item(self, name: str, quantity: int = 1) -> bool:
        """
        Attempts to purchase `quantity` units of `name`.
        Returns True on success (enough stock and balance), otherwise False.
        """
        if name not in self.inventory:
            return False
        item = self.inventory[name]
        if item["quantity"] < quantity:
            return False
        total_price = item["price"] * quantity
        if self.balance < total_price:
            return False
        # perform transaction
        item["quantity"] -= quantity
        self.balance -= total_price
        return True

    def restock_item(self, name: str, quantity: int) -> None:
        """Adds more units to an existing item's stock."""
        if name in self.inventory:
            self.inventory[name]["quantity"] += quantity
        else:
            # If the item didn't exist we create a placeholder with price 0.0
            self.inventory[name] = {"price": 0.0, "quantity": quantity}


class SQLQueryBuilder:
    """
    Generates simple SQL strings from dict inputs.
    All dict iteration follows the `.items()` rule.
    """
    @staticmethod
    def _format_value(v: Any) -> str:
        if isinstance(v, str):
            return f"'{v}'"
        if v is None:
            return "NULL"
        return str(v)

    @staticmethod
    def select(table: str,
               columns: Optional[List[str]] = None,
               where: Optional[Dict[str, Any]] = None) -> str:
        cols_part = "*"
        if columns:
            cols_part = ", ".join(columns)
        sql = f"SELECT {cols_part} FROM {table}"
        if where:
            conditions = []
            for k, v in where.items():
                conditions.append(f"{k} = {SQLQueryBuilder._format_value(v)}")
            sql += " WHERE " + " AND ".join(conditions)
        return sql + ";"

    @staticmethod
    def insert(table: str, data: Dict[str, Any]) -> str:
        keys = []
        vals = []
        for k, v in data.items():
            keys.append(k)
            vals.append(SQLQueryBuilder._format_value(v))
        keys_part = ", ".join(keys)
        vals_part = ", ".join(vals)
        return f"INSERT INTO {table} ({keys_part}) VALUES ({vals_part});"

    @staticmethod
    def update(table: str,
               data: Dict[str, Any],
               where: Optional[Dict[str, Any]] = None) -> str:
        set_parts = []
        for k, v in data.items():
            set_parts.append(f"{k} = {SQLQueryBuilder._format_value(v)}")
        sql = f"UPDATE {table} SET " + ", ".join(set_parts)
        if where:
            conditions = []
            for k, v in where.items():
                conditions.append(f"{k} = {SQLQueryBuilder._format_value(v)}")
            sql += " WHERE " + " AND ".join(conditions)
        return sql + ";"

    @staticmethod
    def delete(table: str, where: Optional[Dict[str, Any]] = None) -> str:
        sql = f"DELETE FROM {table}"
        if where:
            conditions = []
            for k, v in where.items():
                conditions.append(f"{k} = {SQLQueryBuilder._format_value(v)}")
            sql += " WHERE " + " AND ".join(conditions)
        return sql + ";"
>>>>>>> Stashed changes
