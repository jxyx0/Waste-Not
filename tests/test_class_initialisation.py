import unittest
from src.buyer import Buyer
from src.seller import Seller
from src.transaction import Transaction
from src.treasure_bag import TreasureBag


class TestClassInitialisation(unittest.TestCase):
    '''
    Tests for Buyer, Seller, Transaction and TreasureBag classes
    '''
    # Tests for set new data
    def test_set_new_buyer_data(self):
        b = Buyer()
        b.set_new_buyer_data(1, "John", "john@gmail.com", "john1234")

        assert b._id == 1
        assert b._role == "buyer"
        assert b._name == "John"
        assert b._email == "john@gmail.com"
        assert b._password == "john1234"
        assert b._balance == 0.0
        assert b._transactions == []

    def test_set_new_seller_data(self):
        s = Seller()
        s.set_new_seller_data(1, "Nice Cafe", "nicecafe@gmail.com", "nicecafe")

        assert s._id == 1
        assert s._role == "seller"
        assert s._name == "Nice Cafe"
        assert s._email == "nicecafe@gmail.com"
        assert s._password == "nicecafe"
        assert s._balance == 0.0
        assert isinstance(s._treasure_bag, TreasureBag)
        assert s._transactions == []

    def test_set_new_transaction_data(self):
        t = Transaction()
        t.set_new_transaction_data(1, "2025-10-15T10:00:00", 1, 1, 5.99)

        assert t._transaction_id == 1
        assert t._time == "2025-10-15T10:00:00"
        assert t._seller_id == 1
        assert t._buyer_id == 1
        assert t._transaction_amount == 5.99
        assert t._transaction_status == "Active"

    # Test for load_data
    def test_load_transactions(self):
        b = Buyer()
        json_record = {
            "id": 1,
            "role": "buyer",
            "name": "Bob",
            "email": "bob@gmail.com",
            "password": "bread",
            "balance": 200,
            "transactions": [{"transaction_id": 101}]
        }
        t = Transaction()
        t.set_new_transaction_data(101, "2025-10-15T10:00:00", 1, 1, 5.99)
        transaction_data = [t]
        
        transactions = b.load_transactions(json_record["transactions"], transaction_data)

        self.assertEqual(101, transactions[0]._transaction_id)

    def test_load_buyer_data(self):
        b = Buyer()
        json_record = {
            "id": 1,
            "role": "buyer",
            "name": "Bob",
            "email": "bob@gmail.com",
            "password": "bread",
            "balance": 200,
            "transactions": [{"transaction_id": 101}]
        }
        t = Transaction()
        t.set_new_transaction_data(101, "2025-10-15T10:00:00", 1, 1, 5.99)
        transaction_data = [t]

        b.load_data(json_record, transaction_data)

        self.assertEqual(1, b._id)

    def test_load_seller_data(self):
        s = Seller()
        json_record = {
            "id": 2,
            "role": "seller",
            "name": "Bob",
            "email": "bob@gmail.com",
            "password": "bread",
            "balance": 200,
            "treasure_bag": {
                "treasure_bag_id": 2, 
                "price": 5.99, 
                "description": "Pho", 
                "category": "Noodle", 
                "quantity": 5,
                "expiry_time": "2025-10-13T09:30:00"
                },
            "transactions": [{"transaction_id": 101}]
        }
        t = Transaction()
        t.set_new_transaction_data(101, "2025-10-15T10:00:00", 2, 1, 5.99)
        transaction_data = [t]

        s.load_data(json_record, transaction_data)

        self.assertEqual(2, s._id)

    def test_load_treasure_bag_data(self):
        tb = TreasureBag()
        json_record = {
            "treasure_bag_id": 2, 
            "price": 5.99, 
            "discouted_price": 5.99,
            "description": "Pho", 
            "category": "Noodle", 
            "quantity": 5,
            "expiry_time": "2025-10-13T09:30:00"
        }

        tb.load_data(json_record)

        self.assertEqual(2, tb._treasure_bag_id)
