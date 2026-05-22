import unittest
from src.data_mgmt import DataManager
from src.buyer import Buyer
from src.seller import Seller


class TestDataManager(unittest.TestCase):
    def setUp(self):
        self._data_manager = DataManager()

    def test_load_data(self):
        '''
        Check that buyer, seller, and transaction data load successfully.
        '''
        buyers = self._data_manager._buyer_data
        sellers = self._data_manager._seller_data
        transactions = self._data_manager._transaction_data
        assert len(buyers) > 0
        assert len(sellers) > 0
        assert len(transactions) > 0

    def test_register_new_buyer(self):
        '''
        Registering a new buyer should increase buyer count by 1.
        '''
        original_count = len(self._data_manager._buyer_data)
        result = self._data_manager.register("Test Buyer", "buyer@gmail.com", 2, "pass1234")
        self.assertTrue(result)
        self.assertEqual(len(self._data_manager._buyer_data), original_count + 1)

    def test_register_new_seller(self):
        '''
        Registering a new seller should increase seller count by 1.
        '''
        original_count = len(self._data_manager._seller_data)
        result = self._data_manager.register("Test Seller", "seller@gmail.com", 1, "pass1234")
        self.assertTrue(result)
        self.assertEqual(len(self._data_manager._seller_data), original_count + 1)

    def test_register_email_exists(self):
        '''
        Email already registered.
        '''
        original_count = len(self._data_manager._seller_data)
        result = self._data_manager.register("Test Seller", "nicecafe@gmail.com", 1, "pass1234")
        self.assertFalse(result)
        self.assertEqual(len(self._data_manager._seller_data), original_count)

    def test_buyer_login_success(self):
        '''
        Login with existing user should return Buyer.
        '''
        b = Buyer()
        b.set_new_buyer_data(1, "John", "john@gmail.com", "john1234")
        self._data_manager._buyer_data = [b]
        result = self._data_manager.login(b._email, b._password)
        self.assertEqual(b._email, result._email)

    def test_buyer_login_fail(self):
        '''
        Invalid login should return None.
        '''
        result = self._data_manager.login("invalid@example.com", "wrongpassword")
        self.assertEqual(None, result)

    def test_seller_login_success(self):
        '''
        Login with existing user should return Buyer.
        '''
        s = Seller()
        s.set_new_seller_data(1, "Nice Cafe", "nicecafe@gmail.com", "nicecafe")
        self._data_manager._seller_data = [s]
        result = self._data_manager.login(s._email, s._password)
        self.assertEqual(s._email, result._email)

    def test_create_transaction(self):
        original_count = len(self._data_manager._transaction_data)
        b = Buyer()
        b.set_new_buyer_data(1, "John", "john@gmail.com", "john1234")
        s = Seller()
        s.set_new_seller_data(1, "Nice Cafe", "nicecafe@gmail.com", "nicecafe")

        self._data_manager.create_transaction(s._id, b._id, 9.99)

        self.assertEqual(len(self._data_manager._transaction_data), original_count + 1)
        self.assertTrue(any(t._buyer_id == b._id for t in self._data_manager._transaction_data))
        self.assertTrue(any(t._seller_id == s._id for t in self._data_manager._transaction_data))
