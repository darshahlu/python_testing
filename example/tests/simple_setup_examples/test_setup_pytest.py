import pytest


@pytest.fixture(scope='function')
def a_dependency():
    print('\nI am in setup.')
    yield
    # Only runs when "setup" executes without error.
    print('\nNow I am in teardown.')


def test_something(a_dependency):
    print("\nThis is my test code")
    assert True
