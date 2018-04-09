def fib(n):
    """Return the n-th number in the fibonacci series."""
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
    # Is this unittest?
    print(fib(0))
    print(fib(3))
