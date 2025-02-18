""""
描述符
"""


class RequiredString:
    def __init__(self, trim: bool):
        self.__trim = trim

    # set property_name
    def __set_name__(self, owner, name):
        self.__property_name = name

    # set attribute
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise Exception(f"{self.__property_name} is not a string")

        if self.__trim:
            value = value.strip()

        if not len(value):
            raise Exception(f"{self.__property_name} is empty")
        instance.__dict__[self.__property_name] = value

    # get attribute
    def __get__(self, instance, owner):
        if self.__property_name in instance.__dict__:
            return instance.__dict__[self.__property_name]

        raise Exception(f"{self.__property_name} is not exist")
