def singleton1(cls):
    __instance = {}

    def inner():
        if cls not in __instance:
            obj = cls()
            __instance[cls] = obj
        return __instance[cls]
    return inner


def singleton2(cls):

    def inner():
        if not hasattr(cls, "__instance"):
            obj = cls()
            setattr(cls, "__instance", obj)
        return getattr(cls, "__instance")
    return inner


def singleton2(cls):

    def inner():
        if not hasattr(cls, "__instance"):
            obj = cls()
            setattr(cls, "__instance", obj)
        return getattr(cls, "__instance")
    return inner


class SingletonMeta(type):

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "__instance"):
            obj = super().__call__(*args, **kwargs)
            setattr(cls, '__instance', obj)
        return getattr(cls, "__instance")


# @singleton2
# class People:
#     pass
#
#
# p1 = People()
# p2 = People()
# print(p1 is p2)

class People(metaclass=SingletonMeta):
    pass


p1 = People()
p2 = People()
print(p1 is p2)
