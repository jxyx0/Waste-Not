import unittest
from datetime import datetime, timedelta
from hypothesis import given, strategies
from freezegun import freeze_time
from src.business_logic import calculate_freshness_discount


class MockTreasureBag:
    def __init__(self, price, expiry_time):
        self._price = price
        self._discounted_price = price
        self._expiry_time = expiry_time
        self._quantity = 1

class TestFreshnessDiscount(unittest.TestCase):

    # Property-based test using Hypothesis
    @given(
        price=strategies.floats(min_value=0.01, max_value=1000),
        minutes_left=strategies.integers(min_value=-60, max_value=120)
    )
    def test_discount_properties(self, price, minutes_left):
        expiry = datetime.utcnow() + timedelta(minutes=minutes_left)
        bag = MockTreasureBag(price, expiry)
        now = datetime.utcnow()

        calculate_freshness_discount(bag, current_time=now)

        # Discounted price never negative
        self.assertGreaterEqual(bag._discounted_price, 0)

        # Discounted price never exceeds original
        self.assertLessEqual(bag._discounted_price, price)

        # Expired items have 0 quantity
        if minutes_left <= 0:
            self.assertEqual(bag._quantity, 0)
        else:
            self.assertGreater(bag._quantity, 0)

    # Mocked time-based tests using freezegun
    @freeze_time("2025-11-1 10:00:00")
    def test_no_discount_for_fresh_item(self):
        '''No discount if more than 1 hour remains.'''
        bag = MockTreasureBag(100, datetime(2025, 11, 1, 12, 0, 0))
        calculate_freshness_discount(bag)
        self.assertEqual(bag._discounted_price, 100)

    @freeze_time("2025-11-1 11:00:00")
    def test_25_percent_discount(self):
        '''25% discount when 1 hour before expiry.'''
        bag = MockTreasureBag(100, datetime(2025, 11, 1, 12, 0, 0))
        calculate_freshness_discount(bag)
        self.assertEqual(bag._discounted_price, 75.0)

    @freeze_time("2025-11-1 11:30:00")
    def test_50_percent_discount(self):
        '''50% discount when 30 minutes before expiry.'''
        bag = MockTreasureBag(100, datetime(2025, 11, 1, 12, 0, 0))
        calculate_freshness_discount(bag)
        self.assertEqual(bag._discounted_price, 50.0)

    @freeze_time("2025-11-1 12:30:00")
    def test_expired_item_zero_price(self):
        '''Expired items should not be sellable.'''
        bag = MockTreasureBag(100, datetime(2025, 11, 1, 12, 0, 0))
        calculate_freshness_discount(bag)
        self.assertEqual(bag._discounted_price, 0)
        self.assertEqual(bag._quantity, 0)
