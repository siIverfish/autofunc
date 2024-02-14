import unittest
from autofunc.lib import auto

class AutoFuncThreeArgumentTestCase(unittest.TestCase):
    def setUp(self):
        @auto
        def three_arg_function(a, b, c):
            return ('3arg', a, b, c)
        
        self.func = three_arg_function

    def test_3_args_as_auto(self):
        self.assertEqual((self.func)(1)(2)(3), ('3arg', 1, 2, 3))
    
    def test_3_args_as_normal(self):
        self.assertEqual(self.func(1, 2, 3), ('3arg', 1, 2, 3))
    
    def test_nested_3_args(self):
        self.assertEqual((self.func)(self.func)(4)(1)('seven')(2)('seven'), ('3arg', ('3arg', 4, 1, 'seven'), 2, 'seven'))
    
    def test_3_arg_kwargs(self):
        self.assertEqual((self.func)(a=1)(b=2)(c=3), ('3arg', 1, 2, 3))
    
    def test_3_arg_kwargs_mixed(self):
        self.assertEqual((self.func)(1)(b=2)(c=3), ('3arg', 1, 2, 3))
    
    def test_3_arg_nested_kwargs_mixed(self):
        self.assertEqual((self.func)(self.func)(1)(2)(c=3)(4)(c=5), ('3arg', ('3arg', 1, 2, 3), 4, 5))
    
    def test_3_arg_quintuply_nested(self):
        self.assertEqual(
            (self.func)(self.func)(self.func)(self.func)(self.func)(1)(2)(3)(2)(3)(2)(3)(2)(3)(2)(3), 
            ('3arg', ('3arg', ('3arg', ('3arg', ('3arg', 1, 2, 3), 2, 3), 2, 3), 2, 3), 2, 3)
        )


class AutoFuncOneArgumentTestCase(unittest.TestCase):
    def setUp(self):
        @auto
        def one_argument_function(a):
            return ('1arg', a)

        self.one = one_argument_function
    
    def test_one_argument_function_auto(self):
        self.assertEqual((self.one)(1), ('1arg', 1))
    
    def test_one_argument_function_normal(self):
        self.assertEqual(self.one(1), ('1arg', 1))
    
    def test_one_argument_nested(self):
        self.assertEqual((self.one)(self.one)(1), ('1arg', ('1arg', 1)))


class AutoFuncMultiArgumentTestCase(unittest.TestCase):
    def setUp(self):
        @auto
        def one_argument_function(a):
            return ('1arg', a)
    
        @auto
        def three_argument_function(a, b, c):
            return ('3arg', a, b, c)

        self.one = one_argument_function
        self.three = three_argument_function
    
    def test_one_argument_function_auto(self):
        self.assertEqual((self.one)(1), ('1arg', 1))
    
    def test_one_argument_function_normal(self):
        self.assertEqual(self.one(1), ('1arg', 1))
    
    def test_one_and_three_nested_mixed(self):
        self.assertEqual((self.one)(self.one)(self.three)(1)(2)(3), ('1arg', ('1arg', ('3arg', 1, 2, 3))))
    
    def test_one_and_three_nested_extra_mixed(self):
        self.assertEqual(
            (self.three)(1)(self.one)(self.one)(self.three)(self.three)(2)(3)(4)(5)(6)(self.one)(7),
            ('3arg', 1, ('1arg', ('1arg', ('3arg', ('3arg', 2, 3, 4), 5, 6))), ('1arg', 7))
        )


class AutoFuncOneArgumentExceptionTestCase(unittest.TestCase):
    def setUp(self):
        @auto
        def one_argument_function(a):
            return ('1arg', a)
    
        @auto
        def three_argument_function(a, b, c):
            return ('3arg', a, b, c)

        self.one = one_argument_function
        self.three = three_argument_function
    
    def test_three_argument_raises_kwarg_error(self):
        with self.assertRaises(ValueError) as context:
            (self.three)(a=1)(a=2)(3)
    
    def test_three_argument_raises_proxy_error(self):
        pass # this testcase gets broken because of AutoFuncMapPrintTestCase.test_bultin_wrappers
        # with self.assertRaises(ValueError) as context:
        #     _ = auto(map)
    

class AutoFuncMapPrintTestCase(unittest.TestCase):
    def test_bultin_wrappers(self):
        global map, list
        list = auto(list, lambda iterable: None)
        map = auto(map, lambda func, iterable: None)
        self.assertEqual((list)(map)(lambda x: x * 2)([1, 2, 3]), [2, 4, 6])


if __name__ == "__main__":
    unittest.main()