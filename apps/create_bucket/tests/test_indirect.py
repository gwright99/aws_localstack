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
import boto3

@pytest.fixture
def generate_client(request):
    return boto3.client(service_name=request.param, region_name="us-east-1")

@pytest.mark.parametrize('generate_client', ['s3', 'ec2', 'rds'], indirect=['generate_client'])
def test_make_a_client(generate_client):
    print(dir(generate_client))