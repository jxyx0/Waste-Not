class Transaction():
    '''
    Represents a transaction record.

    Every transaction has:
    - an ID (unique)
    - the time the transaction was made
    - the seller's ID
    - the buyer's ID
    - the transaction amount
    - the transaction status (Active, Completed, Expired)
    '''
    def __init__(self):
        '''
        Initialise a new transaction with no data.
        '''
        self._transaction_id = "NO DATA LOADED"
        self._time = "NO DATA LOADED"
        self._seller_id = "NO DATA LOADED"
        self._buyer_id = "NO DATA LOADED"
        self._transaction_amount = "NO DATA LOADED"
        self._transaction_status = "NO DATA LOADED"

    def load_data(self, json_record):
        '''
        Load information about a transaction from JSON.
        '''
        self._transaction_id = int(json_record["transaction_id"])
        self._time = json_record["time"]
        self._seller_id = int(json_record["seller_id"])
        self._buyer_id = int(json_record["buyer_id"])
        self._transaction_amount = float(json_record["transaction_amount"])
        self._transaction_status = json_record["transaction_status"]

    def set_new_transaction_data(self, transaction_id, time, seller_id, buyer_id, transaction_amount):
        '''
        Create a new transaction record with provided details.
        '''
        self._transaction_id = transaction_id
        self._time = time
        self._seller_id = seller_id
        self._buyer_id = buyer_id
        self._transaction_amount = transaction_amount
        self._transaction_status = "Active"

    def __str__(self):
        '''
        Create and return a string representation of the transaction.
        '''
        desc = [f"Transaction ID: {self._transaction_id}"]
        desc.append(f"Transaction Time: {self._time}")
        desc.append(f"Seller ID: {self._seller_id}")
        desc.append(f"Buyer ID: {self._buyer_id}")
        desc.append(f"Transaction Amount: {self._transaction_amount}")
        desc.append(f"Transaction Status: {self._transaction_status}")

        return "\n".join(desc)