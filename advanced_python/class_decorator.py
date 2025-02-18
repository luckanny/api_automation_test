class Decorator:
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        print("start")
        result = self.f(*args, **kwargs)
        print("end")
        return result


class ParaDecorator:
    def __init__(self, var):
        self.var = var

    def __call__(self, f):
        def inner(*args, **kwargs):
            print(f"start {self.var}")
            result = f(*args, **kwargs)
            print("end")
            return result

        return inner


# @Decorator
# def welcom():
#     print("hello")

# @ParaDecorator("parameter")
# def welcom():
#     print("hello")
#
# welcom()
def cls_decorate(cls):
    def inner():
        print("start")
        obj = cls()
        print("end")
        return obj

    return inner


@cls_decorate
class Person:
    pass


p = Person()
