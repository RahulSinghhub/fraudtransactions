from datetime import datetime
from transaction import Transaction
from dynamo_account_profile import DynamoAccountProfile

profile = DynamoAccountProfile()



print(profile.average_amount("A1"))
print(profile.transactions_in_last("A1", 10, datetime.now()))
print(profile.last_known_location("A1"))