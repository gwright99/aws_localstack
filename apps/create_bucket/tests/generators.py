# Examining how generators works to better understand how the pytest fixture factory model works.
# Original pytest factory present in `factory.py`

import pytest

class Customer():

    def __init__(self, name: str, orders: list): 
        self.name = name
        self.orders = orders

    def destroy(self):
        del self


def make_customer_record():

    # This is one of those weird Python things where initializing the tracker here persists across all the calls that
    # are made to it later. Eg.
    # created_records are: [<factory.Customer object at 0x7e2376c2feb0>, <factory.Customer object at 0x7e2376c2fdc0>, <factory.Customer object at 0x7e2376c2fa00>]
    #
    # As per Real Python: https://realpython.com/inner-functions-what-are-they-good-for/
    # """
    # Inner functions, also known as nested functions, are functions that you define inside other functions. 
    # In Python, this kind of function has direct access to variables and names defined in the enclosing function. 
    # Inner functions have many uses, most notably as closure factories and decorator functions."
    #   ...
    # In this section, you’ll learn about closure factory functions. Closures are dynamically created functions 
    # that are returned by other functions. Their main feature is that they have full access to the variables 
    # and names defined in the local namespace where the closure was created, even though the enclosing function 
    # has returned and finished executing.
    # """"
    print('a')
    created_records = []

    def _make_customer_record(name):
        record = Customer(name=name, orders=[])
        created_records.append(record)
        return record

    print('c')
    yield _make_customer_record

    print(f"--------- created_records are: {created_records}")
    for record in created_records:
        print(f"Destroying record {record}")
        record.destroy()


def test_customer_records(somfunc):
    customer_1 = somfunc("Lisa")
    print(f"{customer_1.name} has {customer_1.orders} orders")
    customer_2 = somfunc("Mike")
    print(f"{customer_2.name} has {customer_2.orders} orders")
    customer_3 = somfunc("Meredith")
    print(f"{customer_3.name} has {customer_3.orders} orders")
    print('blah')

# This emits why the pytest setup/teardown works.
print("pre-x")
x = make_customer_record()
print("pre-y")
y = next(x)
print("post-y")
test_customer_records(y)

# Good explanation WHY this works: https://medium.com/geekculture/understand-python-yield-an-interrupter-a-trap-a-scissor-27c2beeed73
try:
    next(x)  # Get past the yield statement
except StopIteration:
    # End of generator. Should see the clean-up portion.
    pass






# Simple self-written generator
def return_square():

    squares = []
    for x in [2,3,4,5]:
        squares.append( x ** 2)
        post_yield_value = yield x ** 2


    print(f"Squares are: {squares}")
    print(f"Post-yield-value is: {post_yield_value}")

s = return_square()
try:
    print(next(s))
    print(next(s))
    print(next(s))
    s.send(890)       # Interesting case. See def below with better explanation.
    print(next(s))
    print(next(s)) # This will fail, cause the print statement, and throw StopIteration exception
except Exception as e:
    print(e)
# except StopIteration:  # This doesnt work
#     s.send(456)


# Generator `send` -- essentially to pass values into a function infinitely (if necessary)
# Ref: https://stackoverflow.com/questions/19302530/what-is-the-purpose-of-the-send-function-on-python-generators

def gen():
    i = 0
    while True:
        # `or i` is used when no arguments provided.`
        i = (yield i) or i
        i += 1

g = gen()
print(next(g))          # 0
print(g.send(5))        # 6
print(next(g))          # 7
print(g.send(10))       # 11
print("------------")


# Example 2
def test_yield_send():
    print("test_yield_send()")

    # The magic of send() is below:

    # 'yield' acts as a placeholder for receiving values from 'send()'
    v = yield  # 'v' receives the value sent to the generator via 'send()'

    # The generator yields 'v' back to the caller of 'send()'
    yield v   # 'v' is returned as the result of 'send()'


print("Hello World!")

# Create a generator object
g = test_yield_send()

# Send a value to the generator
print(g.send(None))  # This prints 'None' because 'v' is set to 'None' now

# Send a value to the generator
print(g.send(2))  # This prints '2' because 'v' is set to '2' now
print("------------")



# Example 3 - best example
# https://python.plainenglish.io/yield-python-part-ii-e93abb619a16

# def prime(generator_fun):
#     '''
#     Method to prime generator function
#     '''
#     generator = generator_fun()
#     next(generator)
#     return generator

# Read print statements to get control loop. Essentially:
# 1) Value is fed in at first yield in loop.
# 2) All logic is processed then we go back to the top of the loop. The processed value is yielded
#    back to the entity which called the generator. Generator becomes suspended again.
# Think of this like the reverse flow of processing.
def running_averager():
    total = 0
    count = 0
    running_average = None
    while True:
        print(f"[TOP_OF_LOOP] Running_average is: {running_average}. Yielding.")
        value = yield running_average # <-- wait for value to be supplied.
        # value = (yield running_average) or running_average  # use local value is next() used instead
        print("Back in generator")
        total += value + 2
        count += 1
        running_average = total/count
        print(f"[BOTTOM_OF_LOOP] Running_average is: {running_average}")

averager = running_averager() # generator creation
print("Priming function")
next(averager) # priming
print("Sending value 10")
print(f"Value returned by called to generator with 10: {averager.send(10)}")   # Result: 10.0
# print(next(averager))      # Wont work with simpler `value` line since func expects a value (since we have only .send as input option)
print("Sending value 20")
print(averager.send(20))   # Result: 15.0
print("Sending value 30")
print(averager.send(30))   # Result: 20.0