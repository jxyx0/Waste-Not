import unittest
from unittest import mock
import src.user_input


class TestUserInput(unittest.TestCase):

    # Tests for is_int
    def test_is_int_with_int(self):
        '''
        Returns True for a valid integer string.
        '''
        self.assertTrue(src.user_input.is_int('1'))

    def test_is_int_with_string(self):
        '''
        Returns False for a non-integer string.
        '''
        self.assertFalse(src.user_input.is_int('abc'))

    # Tests for is_float
    def test_is_float_with_float(self):
        '''
        Returns True for a valid float string.
        '''
        self.assertTrue(src.user_input.is_float('0.5'))

    def test_is_float_with_string(self):
        '''
        Returns False for a non-float string.
        '''
        self.assertFalse(src.user_input.is_float('hello'))

    # Test for read_string
    @mock.patch('builtins.input')
    def test_read_string(self, inp):
        '''
        Returns the provided input.
        '''
        inp.return_value = 'hello'
        self.assertEqual('hello', src.user_input.read_string(''))

    # Tests for read_integer
    @mock.patch('src.user_input.read_string')
    def test_read_integer_with_int(self, readstr):
        '''
        Returns an integer when given a valid integer string.
        '''
        readstr.return_value = '1'
        self.assertEqual(1, src.user_input.read_integer(''))

    @mock.patch('src.user_input.read_string')
    def test_read_integer_with_string(self, readstr):
        '''
        Retry until a valid integer string is given.
        '''
        readstr.side_effect = ['abc', '1']
        self.assertEqual(1, src.user_input.read_integer(''))

    # Tests for read_float
    @mock.patch('src.user_input.read_string')
    def test_read_float_with_float(self, readstr):
        '''
        Returns a float when given a valid float string.
        '''
        readstr.return_value = '0.5'
        self.assertEqual(0.5, src.user_input.read_float(''))

    @mock.patch('src.user_input.read_string')
    def test_read_float_with_string(self, readstr):
        '''
        Retry until a valid float string is given.
        '''
        readstr.side_effect = ['abc', '0.5']
        self.assertEqual(0.5, src.user_input.read_float(''))

    # Tests for read_integer_range
    @mock.patch('src.user_input.read_string')
    def test_read_integer_range_within_range(self, readstr):
        '''
        Test read_integer_range accepts integers within the range.
        '''
        readstr.return_value = '1'
        self.assertEqual(1, src.user_input.read_integer_range('', 0, 10))

    @mock.patch('src.user_input.read_string')
    def test_read_integer_range_out_of_range(self, readstr):
        '''
        Test read_integer_range retries until a value in range is given.
        '''
        readstr.side_effect = ['15', '1']
        self.assertEqual(1, src.user_input.read_integer_range('', 0, 10))

    # Tests for read_bool
    @mock.patch('src.user_input.read_string')
    def test_read_bool_accepts_lower_y(self, readstr):
        '''
        Test read_bool accpets 'y' and returns 'y'.
        '''
        readstr.return_value = 'y'
        self.assertEqual('y', src.user_input.read_bool("Enter y/n: "))

    @mock.patch('src.user_input.read_string')
    def test_read_bool_invalid_input(self, readstr):
        '''
        Test that read_bool keeps prompting until a valid input is given.
        '''
        readstr.side_effect = ['maybe', 'Y']
        self.assertEqual('y', src.user_input.read_bool("Enter y/n: "))

    # Tests for read_password
    @mock.patch('src.user_input.read_string')
    def test_read_password_valid(self, readstr):
        '''
        Test that read_password accepts "abcd1234" and return "abcd1234".
        '''
        readstr.return_value = "abcd1234"
        self.assertEqual("abcd1234", src.user_input.read_password(''))

    @mock.patch('src.user_input.read_string')
    def test_read_password_too_short(self, readstr):
        '''
        Test that read_password keeps prompting until a valid input is given.
        '''
        readstr.side_effect = ["abcd", "abcd1234"]
        self.assertEqual("abcd1234", src.user_input.read_password(''))