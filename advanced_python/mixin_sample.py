import json
import logging

class MapMixin:
    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value


class DictMixin:

    def to_dict(self):
        return self.__convert_dict(self.__dict__)

    def __convert_dict(self, attributes):
        result = {}
        for key, value in attributes.items():
            result[key] = self.__convert_value(value)
        return result

    def __convert_value(self, value):
        if isinstance(value, DictMixin):
            return self.to_dict()
        if isinstance(value, dict):
            return self.__convert_dict(value)
        if isinstance(value, list):
            return [self.__convert_value(x) for x in value]
        else:
            return value


class JSONMixin:
    def to_json(self):
        return json.dumps(self.to_dict())


class Student(MapMixin, DictMixin, JSONMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name},{self.age}"


s = Student("anny", 18)
print(s["name"])
print(s.to_dict())
print(s.to_json())


class LoggerMixin:
    """A mixin class that adds logging functionality to any class."""

    @property
    def logger(self) -> logging.Logger:
        name = '.'.join([self.__module__, self.__class__.__qualname__])
        return logging.getLogger(name)

    def log(self, message: str, level: str = 'info'):
        method = getattr(self.logger, level)
        method(message)


class ShoppingCart(LoggerMixin):
    """Shopping cart class that uses Logger Mixin for logging activities."""

    def add_item(self, item, quantity):
        self.log(f"Added {quantity} of {item} to cart")

    def remove_item(self, item, quantity):
        self.log(f"Removed {quantity} of {item} from cart")


# Configure logging
logging.basicConfig(level=logging.INFO)

cart = ShoppingCart()
cart.add_item("apple", 3)