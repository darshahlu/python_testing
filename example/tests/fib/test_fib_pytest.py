from example.example_library.fib import fib


def test_fib_series():
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(4) == 3
    assert fib(5) == 5


if __name__ == "__main__":
    import pytest

    pytest.main(verbosity=3)
