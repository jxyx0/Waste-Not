from src.treasure_bag import TreasureBag
import src.search as search


class Seller():
    '''
    Represents a seller in the marketplace.

    Every seller has:
    - an ID (unique)
    - a name, email and password
    - a balance
    - a treasure bag they are offering
    - a list of related transactions
    '''
    def __init__(self):
        '''
        Initialise a new seller with no data.
        '''
        self._id = "NO DATA LOADED"
        self._role = "NO DATA LOADED"
        self._name = "NO DATA LOADED"
        self._email = "NO DATA LOADED"
        self._password = "NO DATA LOADED"
        self._balance = "NO DATA LOADED"
        self._treasure_bag = "NO DATA LOADED"
        self._transactions = []

    def load_data(self, json_record, transaction_data):
        '''
        Load information about a seller from JSON.
        '''
        self._id = int(json_record["id"])
        self._role = json_record["role"]
        self._name = json_record["name"]
        self._email = json_record["email"]
        self._password = json_record["password"]
        self._balance = float(json_record["balance"])
        
        self._treasure_bag = TreasureBag()
        self._treasure_bag.load_data(json_record["treasure_bag"])
        self._transactions = self.load_transactions(json_record["transactions"], transaction_data)

    def load_transactions(self, json_record, transaction_data):
        '''
        Load information about a seller's transactions from JSON.
        '''
        transactions = []
        for transaction in json_record:
            transaction_id = int(transaction["transaction_id"])
            t = search.find_transaction_by_id(transaction_id, transaction_data)
            if t is not None:
                transactions.append(t)

        return transactions
    
    def set_new_seller_data(self, id, name, email, password):
        '''
        Create a new seller record with provided details.
        '''
        self._id = id
        self._role = "seller"
        self._name = name
        self._email = email
        self._password = password
        self._balance = 0.0
        self._treasure_bag = TreasureBag()
        self._transactions = []

    def __str__(self):
        '''
        Create and return a string representation of the seller.
        '''
        desc = [f"Seller {self._id}: {self._name} (email: {self._email}, password: {self._password})"]
        desc.append(f"Balance: ${self._balance}")
        desc.append(f"Treasure Bag:")
        desc.append(f"Price: {self._treasure_bag._price}, Description: {self._treasure_bag._description}")
        desc.append(f"Category: {self._treasure_bag._category}, Quantity: {self._treasure_bag._quantity}")

        if len(self._transactions) == 0:
            desc.append("No transactions")
        else:
            desc.append(f"Transactions: {self._transactions}")

        return "\n".join(desc)
