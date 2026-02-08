class WeatherSystem:
<<<<<<< Updated upstream
    def __init__(self, city):
=======
    def __init__(self, city: str):
>>>>>>> Stashed changes
        self.city = city
        self.temperature = 0.0
        self.weather = ""
        self.weather_list = {}

<<<<<<< Updated upstream
    def query(self, weather_list, tmp_units="celsius"):
        self.weather_list = weather_list
        if self.city not in self.weather_list:
            return (0.0, "")
        else:
            info = self.weather_list[self.city]
            self.temperature = info["temperature"]
            self.weather = info["weather"]

        if info["temperature_units"] != tmp_units:
            if tmp_units == "celsius":
                return (self.fahrenheit_to_celsius(), self.weather)
            elif tmp_units == "fahrenheit":
                return (self.celsius_to_fahrenheit(), self.weather)
        else:
            return (self.temperature, self.weather)

    def set_city(self, city):
        self.city = city

    def set_temperature(self, temperature):
=======
    def set_city(self, city: str):
        self.city = city

    def set_temperature(self, temperature: float):
>>>>>>> Stashed changes
        self.temperature = temperature

    def celsius_to_fahrenheit(self):
        return (self.temperature * 9 / 5) + 32

    def fahrenheit_to_celsius(self):
        return (self.temperature - 32) * 5 / 9

    def get_city(self):
        return self.city

    def query(self, weather_list: dict, tmp_units: str = "celsius"):
        """
        weather_list: dict mapping city name to either a WeatherInfo‑like object
        or a dict with keys 'weather', 'temperature', 'temperature_units'.
        Returns a tuple (temperature, weather).
        """
        self.weather_list = weather_list

        entry = self.weather_list.get(self.city)
        if entry is None:
            return 0.0, ""

        # support both object and dict representations
        if isinstance(entry, dict):
            weather = entry.get("weather", "")
            temperature = entry.get("temperature", 0.0)
            units = entry.get("temperature_units", "")
        else:
            # assume attribute access works
            weather = getattr(entry, "weather", "")
            temperature = getattr(entry, "temperature", 0.0)
            units = getattr(entry, "temperature_units", "")

        self.temperature = temperature
        self.weather = weather

        if units != tmp_units:
            if tmp_units == "celsius":
                return self.fahrenheit_to_celsius(), self.weather
            elif tmp_units == "fahrenheit":
                return self.celsius_to_fahrenheit(), self.weather

        return self.temperature, self.weather
