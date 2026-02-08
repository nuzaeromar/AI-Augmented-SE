class CurrencyConverter:
    def __init__(self):
        self.rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.72,
            "JPY": 110.15,
            "CAD": 1.23,
            "AUD": 1.34,
            "CNY": 6.40,
        }
        self.currency_order = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CNY"]

    def convert(self, amount, from_currency, to_currency):
        """
        Convert an amount from one currency to another.

        Returns the converted amount, or None if either currency is unsupported.
        """
        if from_currency == to_currency:
            return amount
        if from_currency not in self.rates or to_currency not in self.rates:
<<<<<<< Updated upstream
            return False
        from_rate = self.rates[from_currency]
        to_rate = self.rates[to_currency]
        converted_amount = (amount / from_rate) * to_rate
        return converted_amount
=======
            return None

        from_rate = self.rates[from_currency]
        to_rate = self.rates[to_currency]

        return (amount / from_rate) * to_rate
>>>>>>> Stashed changes

    def get_supported_currencies(self):
        """Return the list of currency codes in the order they were added."""
        return self.currency_order

    def add_currency_rate(self, currency, rate):
        """
        Add a new currency rate.

        Returns True if the currency was added, False if it already exists.
        """
        if currency in self.rates:
            return False
        self.rates[currency] = rate
        self.currency_order.append(currency)
        return True

    def update_currency_rate(self, currency, new_rate):
        """
        Update an existing currency rate.

        Returns True if the currency exists and was updated, False otherwise.
        """
        if currency not in self.rates:
            return False
        self.rates[currency] = new_rate
        return True
