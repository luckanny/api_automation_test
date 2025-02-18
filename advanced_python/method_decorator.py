# wrapper with parameter
import time


def sleep_time(var):
    def inner(fn):
        def wrapper(*args, **kwargs):
            print(f"sleep time is {var}")
            time.sleep(var)
            result = fn(*args, **kwargs)
            return result
        return wrapper
    return inner


def wrapper_example(fn):
    def wrapper(*args, **kwargs):
        print(f"wrapper_example")
        result = fn(*args, **kwargs)
        return result
    return wrapper


@sleep_time(3)
def test_sleep_time():
    print("test_sleep_time")


@wrapper_example
def test_wrapper():
    print("test_wrapper")


# if __name__ == '__main__':
#     wrapper1()
