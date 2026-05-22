import unittest
import src.business_logic as business_logic
from freezegun import freeze_time
from datetime import datetime, timedelta
from hypothesis import given, strategies


class MockBuyer:
    def __init__(self, balance):
        self._balance = balance

class MockSeller:
    def __init__(self, balance, price, category):
        self._balance = balance
        self._treasure_bag = MockTreasureBag(price, "desc", category, 5)

class MockTreasureBag:
    def __init__(self, price, description, category, quantity):
        self._price = price
        self._discounted_price = price
        self._description = description
        self._category = category
        self._quantity = quantity

class MockTransaction:
    def __init__(self, amount, time):
        self._transaction_amount = amount
        self._time = time
        self._transaction_status = "Active"

class TestH3(unittest.TestCase):

    # Tests for complete_transaction
    @freeze_time("2025-11-02 12:00:00")
    def test_complete_transaction_successful(self):
        '''
        Transaction completed within 1 day.
        '''
        transaction_time = (datetime.utcnow() - timedelta(hours=12)).isoformat()
        transaction = MockTransaction(10, transaction_time)
        seller = MockSeller(0, 5.99, "bread")

        self.assertTrue(business_logic.complete_transaction(transaction, seller))
        self.assertEqual(transaction._transaction_status, "Completed")

    @freeze_time("2025-11-03 12:00:00")
    def test_complete_transaction_expired(self):
        '''
        Transaction expired after 1 day.
        '''
        transaction_time = (datetime.utcnow() - timedelta(days=2)).isoformat()
        transaction = MockTransaction(10, transaction_time)
        seller = MockSeller(0, 5.99, "bread")

        self.assertFalse(business_logic.complete_transaction(transaction, seller))
        self.assertEqual(transaction._transaction_status, "Expired")

    # Test for can_claim_treasure_bag
    @given(
        balance=strategies.floats(min_value=0, max_value=100),
        price=strategies.floats(min_value=1, max_value=50),
        quantity=strategies.integers(min_value=0, max_value=5)
    )
    def test_can_claim_treasure_bag_property(self, balance, price, quantity):
        buyer = MockBuyer(balance)
        bag = MockTreasureBag(price, "desc", "bread", quantity)
        result = business_logic.can_claim_treasure_bag(buyer, bag)
        if balance < price or quantity <= 0:
            self.assertFalse(result)
        else:
            self.assertTrue(result)

    # Test for top_up
    @given(amount=strategies.floats(min_value=-10, max_value=50))
    def test_topup_property(self, amount):
        user = MockBuyer(10)
        result = business_logic.top_up(user, amount)
        if amount > 0:
            self.assertTrue(result)
        else:
            self.assertFalse(result)

    # Test for deposit
    @given(balance=strategies.floats(min_value=0, max_value=100),
        deposit_amount=strategies.floats(min_value=-10, max_value=100))
    def test_deposit_property(self, balance, deposit_amount):
        user = MockBuyer(balance)
        result = business_logic.deposit(user, deposit_amount)
        if deposit_amount <= 0:
            self.assertFalse(result)
        elif deposit_amount <= balance:
            self.assertTrue(result)
        else:
            self.assertFalse(result)
