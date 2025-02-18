class_body = """
def greet(self):
    print("hello customer")

def buy(self):
    print("buy something")
    """
class_dict = {}
exec(class_body, globals(), class_dict)

Customer = type("Customer", (object,), class_dict)
c = Customer()
c.greet()
c.buy()
