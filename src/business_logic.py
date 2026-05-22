from datetime import datetime, timedelta
import src.user_input as user_input


def can_claim_treasure_bag(buyer, treasure_bag):
    if buyer._balance < treasure_bag._discounted_price or treasure_bag._quantity <= 0:
        return False
    
    return True

def claim_treasure_bag(buyer, treasure_bag):
    treasure_bag._quantity -= 1
    buyer._balance -= treasure_bag._discounted_price

def filter_treasure_bags(filter_choice, seller_data):
    filtered_sellers = []

    if filter_choice == 1:
        # Filter by category
        category = user_input.read_string("Enter category to filter by: ").lower()
        for seller in seller_data:
            if seller._treasure_bag._category.lower() == category:
                filtered_sellers.append(seller)

    elif filter_choice == 2:
        # Filter by price range
        max_price = user_input.read_float("Enter maximum price: ")
        while max_price <= 0:
            max_price = user_input.read_float("Enter maximum price: ")
        for seller in seller_data:
            if seller._treasure_bag._discounted_price <= max_price:
                filtered_sellers.append(seller)

    return filtered_sellers

# Functions for seller to update treasure bag
def update_price(treasure_bag, new_price):
    if new_price > 0:
        treasure_bag._price = new_price

def update_description(treasure_bag, new_desc):
    treasure_bag._description = new_desc

def update_category(treasure_bag, new_category):
    treasure_bag._category = new_category

def update_quantity(treasure_bag, new_quantity):
    if new_quantity > 0:
        treasure_bag._quantity = new_quantity

def complete_transaction(transaction_record, seller):
    current_date = datetime.utcnow()
    if current_date > datetime.fromisoformat(transaction_record._time) + timedelta(days=1):
        transaction_record._transaction_status = "Expired"
        seller._balance += transaction_record._transaction_amount
        return False

    transaction_record._transaction_status = "Completed"
    seller._balance += transaction_record._transaction_amount
    return True

def top_up(user, amount):
    if amount <= 0:
        print("Invalid top-up amount.")
        return False
    
    user._balance += amount
    print(f"Successfully topped up ${amount:.2f}. New balance: ${user._balance:.2f}")
    return True

def deposit(user, amount):
    if amount <= 0 or amount > user._balance:
        print("Invalid deposit amount.")
        return False
    
    user._balance -= amount
    print(f"Successfully deposited ${amount:.2f}. Remaining balance: ${user._balance:.2f}")
    return True

def calculate_freshness_discount(treasure_bag, current_time=None):
    '''
    Calculates the discounted price of a treasure bag based on freshness.
    The closer to expiry, the larger the discount.

    Rules:
      - 30 mins before expiry → 50% discount
      - 1 hour before expiry → 25% discount
      - Otherwise → no discount
      - Never return negative prices
    '''
    if current_time is None:
        current_time = datetime.now()

    expiry_time = treasure_bag._expiry_time
    if isinstance(expiry_time, str):
        expiry_time = datetime.fromisoformat(expiry_time)

    original_price = treasure_bag._price
    time_left = expiry_time - current_time

    # Determine discount rate
    if time_left <= timedelta(minutes=0):
        # Already expired: cannot sell
        discounted_price = 0.0
        treasure_bag._quantity = 0
    elif time_left <= timedelta(minutes=30):
        discounted_price = original_price * 0.5
    elif time_left <= timedelta(hours=1):
        discounted_price = original_price * 0.75
    else:
        discounted_price = original_price

    discounted_price = max(0.0, min(discounted_price, original_price))

    treasure_bag._discounted_price = discounted_price
    return discounted_price
