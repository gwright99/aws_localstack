import pytest


### Indirect Parametrization: https://docs.pytest.org/en/latest/example/parametrize.html#indirect-parametrization
# Dont really understand. Trying example.
# 
@pytest.fixture
def fixt(request):
    return request.param * 3


@pytest.mark.parametrize("fixt", ["a", "b"], indirect=True)
def test_indirect(fixt):
    print(f"Fixt is: {fixt}")
    assert len(fixt) == 3

    # Output is:
    # apps/create_bucket/tests/test_s3.py::test_indirect[a] Fixt is: aaa   PASSED
    # apps/create_bucket/tests/test_s3.py::test_indirect[b] Fixt is: bbb   PASSED






@pytest.fixture(scope="function")
def x(request):
    return request.param * 3


@pytest.fixture(scope="function")
def y(request):
    return request.param * 2


# Lack of 'indirect' definition means list-values will go in as literals against the vars. e.g. x='a' rather than x('a')
@pytest.mark.parametrize("x, y", [("a", "b")], indirect=["x"])
def test_indirect2(x, y):
    assert x == "aaa"
    assert y == "b"     
    # IF 'y' also included as indirect
    # FAILED apps/create_bucket/tests/test_indirect.py::test_indirect2[a-b] - AssertionError: assert 'bb' == 'b'


# FROM Stackoverflow - example of how this technique is useful for instantiating classes.
# https://stackoverflow.com/questions/18011902/how-to-pass-a-parameter-to-a-fixture-function-in-pytest
class MyTester:
    def __init__(self, x):
        self.x = x

    def dothis(self):
        assert self.x

@pytest.fixture
def tester(request):
    """Create tester object"""
    return MyTester(request.param)


# Create object MyTester with 'abc' and compare against a literal passed directly into function
@pytest.mark.parametrize('tester, lit', [('abc', 'ABC'), ('def', 'DEF')], indirect=['tester'])
def test_tc1(tester, lit):
       print(tester.x)
       assert (tester.x).upper() == lit


## Trying idea to generate aws clients. This works!!!
# Not sure why I would do this instead of just generating it inside the main test class though. TBD.
import boto3

@pytest.fixture
def generate_client(request):
    return boto3.client(service_name=request.param, region_name="us-east-1")

@pytest.mark.parametrize('generate_client', ['s3', 'ec2', 'rds'], indirect=['generate_client'])
def test_make_a_client(generate_client):
    print(dir(generate_client))




### Another Parametrize example
def data_provider():
    return [
        (1, 2, 3),
        (4, 5, 9),
        (10, -5, 5)
    ]

@pytest.mark.parametrize("a, b, expected_sum", data_provider())
def test_addition(a, b, expected_sum):
    result = a + b
    assert result == expected_sum


# https://docs.pytest.org/en/latest/example/parametrize.html#set-marks-or-test-id-for-individual-parametrized-test
# Use `pytest.mark` to tag tests with metadat for more controlled execution (e.g. quick vs long)
# Use `pytest.param` to add marks and give custom names
# Use `pytest.mark.xfail` to indicate the test is expected to fail (and not cause error).
@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("3+5", 8),
        pytest.param("1+7", 8, marks=pytest.mark.basic),
        pytest.param("2+4", 6, marks=pytest.mark.basic, id="custom_basic_2_plus_4"),
        pytest.param(
            "6*9", 42, marks=[pytest.mark.basic, pytest.mark.xfail], id="basic_expected_to_fail"
        )
    ]
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected


# Parametrize conditional raising (to test out whether certain exceptions are raised or not).
# Note quite sure how that differs from `pytest.mark.xfail`?
# https://docs.pytest.org/en/latest/example/parametrize.html#parametrizing-conditional-raising
from contextlib import nullcontext

# first three test cases should run without any exceptions, while the fourth should raise a``ZeroDivisionError`` exception
@pytest.mark.parametrize(
    "example_input,expectation",
    [
        (3, nullcontext(2)),
        (2, nullcontext(3)),
        (1, nullcontext(6)),
        (0, pytest.raises(ZeroDivisionError)),   # This will throw an error: (KeyError)),
    ],
)
def test_division(example_input, expectation):
    """Test how much I know division."""
    with expectation as e:
        assert (6 / example_input) == e



## Post-Yield Teardown vs `.addfinalizer`
# https://pytest-with-eric.com/pytest-best-practices/pytest-setup-teardown/
# Yield is generally the preferred & straightforward way to teardown. Can use an explicit function though.
# Yield tends to be easier and cleaner for simpler tests; .addfinalizer can be used multiple times for more
# complex teardowns.
# https://docs.pytest.org/en/7.1.x/how-to/fixtures.html#note-on-finalizer-order
# Finalizers are executed in a first-in-last-out order. <-- IMPORTANT
def calculate_square(x):
    return x * x

@pytest.fixture
def setup_data(request):
    print("\nSetting up resources...")
    data = 5
    
    # Define a finalizer function for teardown
    def finalizer():
        print("\nPerforming teardown...")
        # Clean up any resources if needed

    # Register the finalizer to ensure cleanup
    request.addfinalizer(finalizer)

    return data  # Provide the data to the test

# Test cases
def test_square_positive_number(setup_data):
    result = calculate_square(setup_data)
    assert result == 25
    print("Running test case for positive number")

def test_square_negative_number(setup_data):
    result = calculate_square(-setup_data)
    assert result == 25  # The square of -5 is also 25
    print("Running test case for negative number")

