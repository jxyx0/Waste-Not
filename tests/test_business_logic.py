import unittest
import src.business_logic as business_logic
from datetime import datetime, timedelta
from unittest import mock


# Mock classes for isolated testing
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

class TestBusinessLogic(unittest.TestCase):

    def setUp(self):
        self.sellers = [
                    MockSeller(0, 5.99, "bread"),
                    MockSeller(0, 10.99, "bread"),
                    MockSeller(0, 10, "noodle"),
                    MockSeller(0, 15, "japanese")
                ]

    # Tests for can_claim_treasure_bag
    def test_cannot_claim_bag_balance_5(self):
        '''
        Buyer balance below price
        '''
        buyer = MockBuyer(5)
        bag = MockTreasureBag(10, "baked goods", "bread", 1)
        self.assertEqual(business_logic.can_claim_treasure_bag(buyer, bag), False)

    def test_cannot_claim_bag_balance_9_99(self):
        '''
        Buyer balance slightly below price
        '''
        buyer = MockBuyer(9.99)
        bag = MockTreasureBag(10, "baked goods", "bread", 1)
        self.assertEqual(business_logic.can_claim_treasure_bag(buyer, bag), False)

    def test_can_claim_bag_exact_balance(self):
        '''
        Buyer balance exactly same as price
        '''
        buyer = MockBuyer(10)
        bag = MockTreasureBag(10, "baked goods", "bread", 1)
        self.assertEqual(business_logic.can_claim_treasure_bag(buyer, bag), True)

    def test_can_claim_bag_balance_10_01(self):
        '''
        Buyer balance slightly above price
        '''
        buyer = MockBuyer(10.01)
        bag = MockTreasureBag(10, "baked goods", "bread", 1)
        self.assertEqual(business_logic.can_claim_treasure_bag(buyer, bag), True)

    def test_can_claim_bag_balance_20(self):
        '''
        Buyer balance above price
        '''
        buyer = MockBuyer(20)
        bag = MockTreasureBag(10, "baked goods", "bread", 1)
        self.assertEqual(business_logic.can_claim_treasure_bag(buyer, bag), True)

    def test_cannot_claim_bag_out_of_stock(self):
        '''
        Treasure bag out of stock
        '''
        buyer = MockBuyer(20)
        bag = MockTreasureBag(10, "baked goods", "bread", 0)
        self.assertEqual(business_logic.can_claim_treasure_bag(buyer, bag), False)

    # Tests for claim_treasure_bag
    def test_claim_treasure_bag_updates(self):
        '''
        Claiming treasure bag reduces buyer balance and bag quantity
        '''
        buyer = MockBuyer(20)
        bag = MockTreasureBag(10, "baked goods", "bread", 2)
        business_logic.claim_treasure_bag(buyer, bag)
        self.assertEqual(buyer._balance, 10)
        self.assertEqual(bag._quantity, 1)

    # Tests for filter_treasure_bags
    @mock.patch('src.user_input.read_string')
    def test_filter_by_category_match(self, readstr):
        '''
        Buyer filters by category, return only treasure bags with matching category
        '''
        readstr.return_value = "bread"
        result = business_logic.filter_treasure_bags(1, self.sellers)
        self.assertEqual(2, len(result))

    @mock.patch('src.user_input.read_string')
    def test_filter_by_category_no_match(self, readstr):
        '''
        Buyer filters by category, no treasure bags match the category
        '''
        readstr.return_value = "sushi"
        result = business_logic.filter_treasure_bags(1, self.sellers)
        self.assertEqual(0, len(result))

    @mock.patch('src.user_input.read_float')
    def test_filter_by_price_range(self, readfloat):
        '''
        Buyer filters by price range, return all treasure bags with price below max
        '''
        readfloat.return_value = 10
        result = business_logic.filter_treasure_bags(2, self.sellers)
        self.assertEqual(2, len(result))

    @mock.patch('src.user_input.read_float')
    def test_filter_by_price_range_negative(self, readfloat):
        '''
        Buyer filters by negative price range,
        keeps prompting until a valid input is given
        '''
        readfloat.side_effect = [-1, 10]
        result = business_logic.filter_treasure_bags(2, self.sellers)
        self.assertEqual(2, len(result))

    def test_invalid_filter_choice(self):
        '''
        Return empty list if an invalid filter choice is given
        '''
        result = business_logic.filter_treasure_bags(999, self.sellers)
        self.assertEqual([], result)

    # Tests for seller updating treasure bag
    def test_update_price(self):
        '''
        Price is updated
        '''
        bag = MockTreasureBag(10, "baked goods", "bread", 1)
        business_logic.update_price(bag, 15)
        self.assertEqual(bag._price, 15)

    def test_update_price_negative(self):
        '''
        Price is not updated if the new price is negative
        '''
        bag = MockTreasureBag(10, "baked goods", "bread", 1)
        business_logic.update_price(bag, -10)
        self.assertEqual(bag._price, 10)

    def test_update_description(self):
        '''
        Description is updated
        '''
        bag = MockTreasureBag(10, "old desc", "bread", 1)
        business_logic.update_description(bag, "new desc")
        self.assertEqual(bag._description, "new desc")

    def test_update_category(self):
        '''
        Category is updated
        '''
        bag = MockTreasureBag(10, "bevarage", "bread", 1)
        business_logic.update_category(bag, "drinks")
        self.assertEqual(bag._category, "drinks")

    def test_update_quantity(self):
        '''
        Quantity is updated
        '''
        bag = MockTreasureBag(10, "baked goods", "bread", 1)
        business_logic.update_quantity(bag, 5)
        self.assertEqual(bag._quantity, 5)

    def test_update_quantity_negative(self):
        '''
        Quantity is not updated if the new quantity is negative
        '''
        bag = MockTreasureBag(10, "baked goods", "bread", 1)
        business_logic.update_quantity(bag, -1)
        self.assertEqual(bag._quantity, 1)

    # Tests for complete_transaction
    def test_complete_transaction_successful(self):
        '''
        Transaction completed within 1 day
        '''
        time = datetime.utcnow().isoformat()
        transaction = MockTransaction(10, time)
        seller = MockSeller(0, 5.99, "bread")
        self.assertTrue(business_logic.complete_transaction(transaction, seller))
        self.assertEqual(transaction._transaction_status, "Completed")
        self.assertEqual(seller._balance, 10)
    
    def test_complete_transaction_expired(self):
        '''
        Transaction expired after 1 day
        '''
        expired_time = (datetime.utcnow() - timedelta(days=2)).isoformat()
        transaction = MockTransaction(10, expired_time)
        seller = MockSeller(0, 5.99, "bread")

        self.assertFalse(business_logic.complete_transaction(transaction, seller))
        self.assertEqual(transaction._transaction_status, "Expired")
        self.assertEqual(seller._balance, 10)

    # Tests for top_up
    def test_topup_positive_amount(self):
        '''
        Valid top-up amount return True
        '''
        user = MockBuyer(10)
        self.assertEqual(business_logic.top_up(user, 5), True)

    def test_topup_invalid_zero_amount(self):
        '''
        Zero top-up amount should return False
        '''
        user = MockBuyer(10)
        self.assertEqual(business_logic.top_up(user, 0), False)

    def test_topup_invalid_negative_amount(self):
        '''
        Negative top-up amount should return False
        '''
        user = MockBuyer(10)
        self.assertEqual(business_logic.top_up(user, -5), False)

    # Tests for deposit
    def test_deposit_positive_amount(self):
        '''
        Deposit amount lesser than balance should return True
        '''
        user = MockBuyer(50)
        self.assertEqual(business_logic.deposit(user, 5), True)

    def test_deposit_invalid_zero_amount(self):
        '''
        Zero deposit amount should return False
        '''
        user = MockBuyer(50)
        self.assertEqual(business_logic.deposit(user, 0), False)

    def test_deposit_invalid_negative_amount(self):
        '''
        Negative deposit amount should return False
        '''
        user = MockBuyer(50)
        self.assertEqual(business_logic.deposit(user, -5), False)

    def test_deposit_amount_49_9(self):
        '''
        Deposit amount slightly lesser than balance should return True
        '''
        user = MockBuyer(50)
        self.assertEqual(business_logic.deposit(user, 49.9), True)

    def test_deposit_amount_50(self):
        '''
        Deposit amount exactly same as balance should return True
        '''
        user = MockBuyer(50)
        self.assertEqual(business_logic.deposit(user, 50), True)

    def test_deposit_amount_50_1(self):
        '''
        Deposit amount slightly larger than balance should return False
        '''
        user = MockBuyer(50)
        self.assertEqual(business_logic.deposit(user, 50.1), False)

    def test_deposit_amount_70(self):
        '''
        Deposit amount larger than balance should return False
        '''
        user = MockBuyer(50)
        self.assertEqual(business_logic.deposit(user, 70), False)