class TreasureBag():
    '''
    Represents a treasure bag that a seller offers in the marketplace.

    Every treasure bag has:
    - an ID (unique)
    - a price
    - a description
    - a category
    - a quantity available
    - expiry time of the items
    '''
    def __init__(self):
        '''
        Initialise a new treasure bag with no data.
        '''
        self._treasure_bag_id = "NO DATA LOADED"
        self._price = "NO DATA LOADED"
        self._discounted_price = "NO DATA LOADED"
        self._description = "NO DATA LOADED"
        self._category = "NO DATA LOADED"
        self._quantity = "NO DATA LOADED"
        self._expiry_time = "NO DATA LOADED"

    def load_data(self, json_record):
        '''
        Load information about a treasure bag from JSON.
        '''
        self._treasure_bag_id = int(json_record["treasure_bag_id"])
        self._price = float(json_record["price"])
        self._discounted_price = float(json_record["price"])
        self._description = json_record["description"]
        self._category = json_record["category"]
        self._quantity = int(json_record["quantity"])
        self._expiry_time = json_record["expiry_time"]

    def __str__(self):
        '''
        Create and return a string representation of the treasure bag.
        '''
        if self._discounted_price == self._price:
            desc = [f"Treasure Bag:"]
            desc.append(f"Price: ${self._price:.2f}")
            desc.append(f"Description: {self._description}")
            desc.append(f"Category: {self._category}")
            desc.append(f"Quantity: {self._quantity}")
            desc.append(f"Expiry time: {self._expiry_time}")
        else:
            desc = [f"Treasure Bag:"]
            desc.append(f"Discounted price: ${self._discounted_price:.2f} (original ${self._price:.2f})")
            desc.append(f"Description: {self._description}")
            desc.append(f"Category: {self._category}")
            desc.append(f"Quantity: {self._quantity}")
            desc.append(f"Expiry time: {self._expiry_time}")

        return "\n".join(desc)
