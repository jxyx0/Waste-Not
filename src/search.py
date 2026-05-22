def find_transaction_by_id(transaction_id, transaction_data):
    found = None

    for t in transaction_data:
        if t._transaction_id == transaction_id:
            found = t

    return found

def find_treasure_bag_by_seller_id(seller_id, seller_data):
    found = None

    for s in seller_data:
        if s._id == seller_id:
            found = s._treasure_bag

    return found
