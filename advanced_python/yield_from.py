def exponent(exponent_number: int):
    for i in range(3):
        yield (i+1)**exponent_number


def magic():
    yield from exponent(2)
    yield from exponent(3)


# g = magic()
# for i in g:
#     print(i)


def magic2():
    exponent_number = yield "please give a exponent number based two"
    while True:
        exponent_number = yield 2 ** exponent_number

        if exponent is None:
            break

# g = magic2()
# print(next(g))
# print(g.send(2))
# print(g.send(4))
# g.send(g.send(5))
# try:
#     g.send(None)
# except:
#     pass


def magic3():
    exponent_number = yield "please give a exponent number based on three"
    while True:
        exponent_number = yield 3 ** exponent_number

        if exponent is None:
            break


def magic_switch():
    choice_number = yield "please choice,1 is 2 ,2 is 3",
    while True:
        if choice_number == 1:
            yield from magic2()
        elif choice_number == 2:
            yield from magic3()
        else:
            break


g = magic_switch()
print(next(g))
print(g.send(1))
print(g.send(2))
print(g.send(4))
print(g.send(5))

try:
    print(g.send(None))
except:
    pass

