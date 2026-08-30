from datetime import datetime
from transaction import Transaction
from dynamo_account_profile import DynamoAccountProfile

profile = DynamoAccountProfile()
txn = Transaction("t1", "A2", 500, "grocery", "Bengaluru", datetime.now())
profile.record(txn)
print("Recorded successfully")


profile.average_amount("A2")
profile.transactions_in_last("A2", 10, datetime.now())
profile.last_known_location("A2")