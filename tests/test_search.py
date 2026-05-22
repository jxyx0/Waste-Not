import unittest
import src.search as search


# Mock classes for isolated testing
class MockTransaction:
    def __init__(self, transaction_id):
        self._transaction_id = transaction_id

class MockTreasureBag:
    def __init__(self, treasure_bag_id):
        self._treasure_bag_id = treasure_bag_id

class MockSeller:
    def __init__(self, id, treasure_bag):
        self._id = id
        self._treasure_bag = treasure_bag

class TestSearch(unittest.TestCase):
    # Tests for find_transaction_by_id
    def test_find_transaction_by_id_found(self):
        '''
        Return the transaction object when ID matches.
        '''
        t1 = MockTransaction(101)
        t2 = MockTransaction(102)
        transaction_data = [t1, t2]

        result = search.find_transaction_by_id(102, transaction_data)
        self.assertEqual(result, t2)

    def test_find_transaction_by_id_not_found(self):
        '''
        Return None if no transaction with matching ID.
        '''
        t1 = MockTransaction(101)
        t2 = MockTransaction(102)
        transaction_data = [t1, t2]

        result = search.find_transaction_by_id(999, transaction_data)
        self.assertIsNone(result)

    def test_find_transaction_by_id_empty_list(self):
        '''
        Return None hen transaction list is empty.
        '''
        result = search.find_transaction_by_id(101, [])
        self.assertIsNone(result)

    # Tests for find_treasure_bag_by_seller_id
    def test_find_treasure_bag_by_seller_id_found(self):
        '''
        Return the correct treasure bag when seller ID matches.
        '''
        bag1 = MockTreasureBag(1)
        bag2 = MockTreasureBag(2)
        seller1 = MockSeller(1, bag1)
        seller2 = MockSeller(2, bag2)
        sellers = [seller1, seller2]

        result = search.find_treasure_bag_by_seller_id(2, sellers)
        self.assertEqual(result, bag2)

    def test_find_treasure_bag_by_seller_id_not_found(self):
        '''
        Return None when no seller matches the ID.
        '''
        bag1 = MockTreasureBag(1)
        sellers = [MockSeller(1, bag1)]

        result = search.find_treasure_bag_by_seller_id(99, sellers)
        self.assertIsNone(result)

    def test_find_treasure_bag_by_seller_id_empty_list(self):
        '''
        Return None when seller list is empty.
        '''
        result = search.find_treasure_bag_by_seller_id(1, [])
        self.assertIsNone(result)