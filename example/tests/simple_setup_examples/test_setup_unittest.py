import unittest


class TestStuff(unittest.TestCase):

    def setUp(self):
        print('\nI am in setup.')

    def tearDown(self):
        print('\nNow I am in teardown.')

    def test_something(self):
        print("\nThis is my test code")
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
