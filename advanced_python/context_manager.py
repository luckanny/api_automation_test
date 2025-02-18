import time
from contextlib import contextmanager


class Timer:
    def __init__(self):
        self.elapse = 0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        self.elapse = self.end-self.start


"""
with Timer()创建一个对象并执行Timer这个类中的enter方法，并将返回值付给timer
执行完成后自动调用exit方法
"""
with Timer() as timer:
    lista = []
    for i in range(10000):
        lista.append(i**2)

print(timer.elapse)


# @contextmanager
# def managed_file(filename, mode):
#     try:
#         file = open(filename, mode)
#         yield file
#     finally:
#         file.close()
#
# # 使用简化的上下文管理器
# with managed_file("example.txt", "w") as file:
#     file.write("Hello again, World!")


@contextmanager
def timer():
    try:
        start = time.perf_counter()
        yield
    finally:
        end = time.perf_counter()
        elapse = end - start
        print(elapse)

"""
在 yield 之前的代码块可以看作是 __enter__ 方法的身体，而在 yield 之后的代码块可以看作是 __exit__ 方法的身体。
"""
with timer() as timer:
    lista = []
    for i in range(10000):
        lista.append(i**2)
