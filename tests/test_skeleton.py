import unittest

from python320_todoapp.skeleton import fib, main

__author__ = "Carl Parker"
__copyright__ = "Carl Parker"
__license__ = "MIT"


class TestSk(unittest.TestCase):

    def test_fib(self):
        """API Tests"""
        assert fib(1) == 1
        assert fib(2) == 1
        assert fib(7) == 13
        return( True )


    # def test_main(capsys):
    #     """CLI Tests"""
    #     # capsys is a pytest fixture that allows asserts against stdout/stderr
    #     # https://docs.pytest.org/en/stable/capture.html
    #     main(["7"])
    #     captured = capsys.readouterr()
    #     assert "The 7-th Fibonacci number is 13" in captured.out
