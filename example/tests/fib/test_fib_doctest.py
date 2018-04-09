# This doctest would normally appear in the production code only (e.g. in example_library/fib.py module).
# The fib method and doctest is copied here just to keep this example in the same directory as the other example tests.
def fib(n):
    """Return the n-th number in the fibonacci series.

    >>> fib(0)
    0
    >>> fib(1)
    1
    >>> fib(2)
    1
    >>> fib(3)
    2
    >>> fib(4)
    3
    >>> fib(5)
    5
    >>> fib(29)
    514229
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
