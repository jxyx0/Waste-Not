'''
Some portions of this code are inspired by code from BAT
by Dr. Charlotte Pierce.
'''


import json
import sys

from src.buyer import Buyer
from src.seller import Seller
from src.transaction import Transaction
from src.treasure_bag import TreasureBag
import src.config as config
import datetime


class DataManager():
    '''
    Manages buyer, seller and transaction data.
    '''
    def __init__(self):
        '''
        Create a new data manager, loading data from the files
        specified in the software configuration.
        '''
        self._transaction_data = None
        self.load_transactions()
        self._buyer_data = None
        self.load_buyers()
        self._seller_data = None
        self.load_sellers()
        self._treasure_bags_data = None
        self.load_treasure_bags()

    def register(self, user_name, user_email, user_role, user_password):
        '''
        Handles storing a new user if email not already registered.
        '''
        # If user already exists
        if self.exists(user_email):
            return False
        
        # If user is seller
        if user_role == 1:
            next_id = max(self._seller_data, key=lambda p: p._id)._id + 1
        
            new_seller = Seller()
            new_seller.set_new_seller_data(next_id, user_name, user_email, user_password)

            self._seller_data.append(new_seller)

            return True
        
        # If user is buyer
        elif user_role == 2:
            next_id = max(self._buyer_data, key=lambda p: p._id)._id + 1
        
            new_buyer = Buyer()
            new_buyer.set_new_buyer_data(next_id, user_name, user_email, user_password)

            self._buyer_data.append(new_buyer)

            return True

    def exists(self, user_email):
        for seller in self._seller_data:
            if seller._email == user_email:
                return True
            
        for buyer in self._buyer_data:
            if buyer._email == user_email:
                return True
            
        return False
    
    def login(self, user_email, user_password):
        for seller in self._seller_data:
            if seller._email == user_email and seller._password == user_password:
                return seller
            
        for buyer in self._buyer_data:
            if buyer._email == user_email and buyer._password == user_password:
                return buyer
            
        return None
    
    def create_transaction(self, seller_id, buyer_id, transaction_amount):
        if self._transaction_data:
            next_id = max(self._transaction_data, key=lambda p: p._transaction_id)._transaction_id + 1
        else:
            next_id = 101

        t = Transaction()
        t.set_new_transaction_data(
            next_id,
            datetime.datetime.now().isoformat(timespec='seconds'),
            seller_id,
            buyer_id,
            transaction_amount
        )

        self._transaction_data.append(t)

        for seller in self._seller_data:
            if seller._id == seller_id:
                seller._transactions.append(t)

        for buyer in self._buyer_data:
            if buyer._id == buyer_id:
                buyer._transactions.append(t)

    def load_buyers(self):
        try:
            with open(config.BUYER_DATA, 'r') as f:
                data = json.load(f)

            buyers = []
            for d in data:
                new_buyer = Buyer()
                new_buyer.load_data(d, self._transaction_data)
                buyers.append(new_buyer)

            self._buyer_data = buyers
        except:
            print("ERROR LOADING BUYER DATA: EXITING.")
            sys.exit()

    def save_buyers(self):
        with open(config.BUYER_DATA, 'w') as f:
            f.write("[")
            for b in self._buyer_data:
                f.write(json.dumps(b, cls=self.BuyerEncoder))
                if b != self._buyer_data[-1]:
                    f.write(",")
            f.write("]")

    def load_sellers(self):
        try:
            with open(config.SELLER_DATA, 'r') as f:
                data = json.load(f)

            sellers = []
            for d in data:
                new_seller = Seller()
                new_seller.load_data(d, self._transaction_data)
                sellers.append(new_seller)

            self._seller_data = sellers
        except:
            print("ERROR LOADING SELLER DATA: EXITING.")
            sys.exit()

    def save_sellers(self):
        with open(config.SELLER_DATA, 'w') as f:
            f.write("[")
            for s in self._seller_data:
                f.write(json.dumps(s, cls=self.SellerEncoder))
                if s != self._seller_data[-1]:
                    f.write(",")
            f.write("]")

    def load_transactions(self):
        try:
            with open(config.TRANSACTION_DATA, 'r') as f:
                data = json.load(f)

            transactions = []
            for d in data:
                new_transaction = Transaction()
                new_transaction.load_data(d)
                transactions.append(new_transaction)

            self._transaction_data = transactions
        except:
            print("ERROR LOADING TRANSACTION DATA: EXITING.")
            sys.exit()

    def save_transactions(self):
        with open(config.TRANSACTION_DATA, 'w') as f:
            f.write("[")
            for t in self._transaction_data:
                f.write(json.dumps(t, cls=self.TransactionEncoder))
                if t != self._transaction_data[-1]:
                    f.write(",")
            f.write("]")

    def load_treasure_bags(self):
        try:
            with open(config.SELLER_DATA, 'r') as f:
                data = json.load(f)

            treasure_bags = []
            for d in data:
                new_treasure_bag = TreasureBag()
                new_treasure_bag.load_data(d["treasure_bag"])
                treasure_bags.append({
                    "seller_id": d["id"],
                    "seller_name": d["name"],
                    "treasure_bag": new_treasure_bag
                })

            self._treasure_bags_data = treasure_bags
        except:
            print("ERROR LOADING TREASURE BAGS: EXITING.")
            sys.exit()

    class BuyerEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Buyer):
                return {
                    "id": obj._id,
                    "role": obj._role,
                    "name": obj._name,
                    "email": obj._email,
                    "password": obj._password,
                    "balance": obj._balance,
                    "transactions": [
                        {
                            "transaction_id": t._item._transaction_id,
                            "time": t._time.strftime('%d %b %Y, %H:%M UTC'),
                            "seller_id": t._seller_id,
                            "transaction_status": t._transaction_status
                        } for t in obj._transactions
                    ]
                }
            return super().default(obj)
        
    class SellerEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Seller):
                return {
                    "id": obj._id,
                    "role": obj._role,
                    "name": obj._name,
                    "email": obj._email,
                    "password": obj._password,
                    "balance": obj._balance,
                    "treasure_bag": obj._treasure_bag,
                    "transactions": [
                        {
                            "transaction_id": t._transaction_id,
                            "time": t._time.strftime('%d %b %Y, %H:%M UTC'),
                            "buyer_id": t._buyer_id,
                            "transaction_status": t._transaction_status
                        } for t in obj._transactions
                    ]
                }
            return super().default(obj)
        
    class TransactionEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Transaction):
                return {
                    "transaction_id": obj._transaction_id,
                    "time": obj._time,
                    "seller_id": obj._seller_id,
                    "buyer_id": obj._buyer_id,
                    "transaction_status": obj._transaction_status,
                }
            return super().default(obj)
