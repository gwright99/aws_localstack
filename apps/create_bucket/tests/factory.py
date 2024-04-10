import pytest

class Customer():

    def __init__(self, name: str, orders: list): 
        self.name = name
        self.orders = orders

    def destroy(self):
        del self


@pytest.fixture
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
    created_records = []

    def _make_customer_record(name):
        record = Customer(name=name, orders=[])
        created_records.append(record)
        return record

    yield _make_customer_record

    print(f"--------- created_records are: {created_records}")
    for record in created_records:
        record.destroy()


def test_customer_records(make_customer_record):
    customer_1 = make_customer_record("Lisa")
    customer_2 = make_customer_record("Mike")
    customer_3 = make_customer_record("Meredith")


def test_assert_one_one():
    assert 1 == 1