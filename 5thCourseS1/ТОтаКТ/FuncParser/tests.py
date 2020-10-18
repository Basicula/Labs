import unittest
import numpy as np
from shuting_yard import *

class ShutingYardArithmeticOperationsTests(unittest.TestCase):
    def test_plus_operator(self):
        print("\nPlus operator", end = "")
        func = ShutingYard("2+2")
        actual = func(0)
        expected = 4
        self.assertEqual(actual, expected)
        
    def test_minus_operator(self):    
        print("\nMinus operator", end = "")
        func = ShutingYard("3-123")
        actual = func(0)
        expected = -120
        self.assertEqual(actual, expected)
        
    def test_product_operator(self):    
        print("\nProduct operator", end = "")
        func = ShutingYard("3 * 21")
        actual = func(0)
        expected = 63
        self.assertEqual(actual, expected)
        
    def test_divide_operator(self):    
        print("\nDivide operator", end = "")
        func = ShutingYard("18 / 3")
        actual = func(0)
        expected = 6
        self.assertEqual(actual, expected)
    
    def test_all_arithmetic_operations(self):
        print("\nAll arithmetic operators in one expression", end = "")
        func = ShutingYard("2 + 2 * 2 - 16 / 4 / 2")
        actual = func(0)
        expected = 4
        self.assertEqual(actual, expected)
        
    def test_wrong_arithmetic_expression(self):
        print("\nWrong arithmetic expression", end = "")
        
        with self.assertRaises(Exception):
            func = ShutingYard("2 +")
            
        with self.assertRaises(Exception):
            func = ShutingYard("+-/*")
        
        with self.assertRaises(Exception):
            func = ShutingYard("+-2/*")
            
        with self.assertRaises(Exception):
            func = ShutingYard("2++2")
            
        with self.assertRaises(Exception):
            func = ShutingYard("2--2")
            
        with self.assertRaises(Exception):
            func = ShutingYard("(2 + 3")
            
        with self.assertRaises(Exception):
            func = ShutingYard("(2 + 3))")
            
        with self.assertRaises(Exception):
            func = ShutingYard("someotherfunc(x)")
        
class ShutingYardFunctionsTests(unittest.TestCase):
    def test_abs_function(self):
        print("\nAbs function", end = "")
        func = ShutingYard("abs(x)")
        actual = func(-2)
        expected = 2
        self.assertEqual(actual, expected)

    def test_cos_function(self):
        print("\nCos function", end = "")
        func = ShutingYard("cos(x)")
        actual = func(0)
        expected = 1
        self.assertEqual(actual, expected)

    def test_sin_function(self):
        print("\nSin function", end = "")
        func = ShutingYard("sin(x)")
        actual = func(math.pi / 2)
        expected = 1
        self.assertEqual(actual, expected)
        
    def test_exp_function(self):
        print("\nExp function", end = "")
        func = ShutingYard("exp(x)")
        actual = func(0)
        expected = 1
        self.assertEqual(actual, expected)
        
        actual = func(1)
        expected = math.e
        self.assertEqual(actual, expected)

    def test_pow_function(self):
        print("\nPow function", end = "")
        func = ShutingYard("pow(x, 2)")
        actual = func(2)
        expected = 4
        self.assertEqual(actual, expected)
        
    def test_sqrt_function(self):
        print("\nSqrt function", end = "")
        func = ShutingYard("sqrt(x)")
        actual = func(4)
        expected = 2
        self.assertEqual(actual, expected)
        
    def test_tg_function(self):
        print("\nSin function", end = "")
        func = ShutingYard("tg(x)")
        actual = round(func(math.pi / 4),10)
        expected = 1
        self.assertEqual(actual, expected)
        
    def test_all_functions(self):
        print("\nAll functions in one expression", end = "")
        func = ShutingYard("abs(cos(sin(x)) * tg(x) + pow(x, exp(x)) - sqrt(4))")
        actual = func(0)
        expected = 2
        self.assertEqual(actual, expected)    
        
class ShutinYardUsageTests(unittest.TestCase):
    def test_arguments_reuse(self):
        print("\nReuse expression for different arguments", end = "")
        func = ShutingYard("x * sqrt(x)")
        actual = func(4)
        expected = 8
        self.assertEqual(actual, expected)
        
        actual = func(16)
        expected = 64
        self.assertEqual(actual, expected)
        
    def test_numpy_integration(self):
        print("\nNumpy integration", end = "")
        func = ShutingYard("x + sqrt(x)")
        x = np.array([4,9,16])
        actual = func(x)
        expected = np.array([6, 12, 20])
        self.assertTrue(np.array_equal(actual, expected))
        
if __name__ == "__main__":
    unittest.main()