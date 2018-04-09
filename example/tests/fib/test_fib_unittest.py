import unittest

from example.example_library.fib import fib


class TestStuff(unittest.TestCase):

    def test_fib_series(self):
        self.assertEqual(fib(0), 0)
        self.assertEqual(fib(1), 1)
        self.assertEqual(fib(2), 1)
        self.assertEqual(fib(3), 2)
        self.assertEqual(fib(4), 3)
        self.assertEqual(fib(5), 5)


if __name__ == "__main__":
    unittest.main()
