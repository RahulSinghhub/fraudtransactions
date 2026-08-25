from transaction import Transaction
from datetime import timedelta
from account_profile import AccountProfile

"""
the rules will have same parameter where they are given an accountid and the profile information and
return type will be string that explain the constraint and weight that is given
"""
def rule_large_amount(txn : Transaction, profile : AccountProfile, now):
    if txn.amount > (5 * profile.average_amount(txn.account_id)) and profile.average_amount(txn.account_id) != 0:
        return ("large transaction amount", 40)
    return None

def rule_odd_hour(txn : Transaction, profile : AccountProfile, now):
    if (txn.hour_of_day() < 5) or (txn.hour_of_day() >= 23):
        return ("transaction at odd time", 15)
    return None

def rule_velocity(txn : Transaction, profile : AccountProfile, now):
    if len(profile.transactions_in_last(txn.account_id, 10, now)) >= 4:
        return ("more than 4 transactions done", 35)
    return None


def rule_impossible_travel(txn : Transaction, profile : AccountProfile, now):
    last_city = profile.last_known_location(txn.account_id)
    if last_city is None:
        return None
    time_gap_minutes = (now - last_city[1]).total_seconds() / 60
    if txn.city != last_city[0] and (time_gap_minutes < 30):
        return ("transaction is impossible because of travel distance", 50)
    return None

ALL_RULES = [
    rule_large_amount,
    rule_odd_hour,
    rule_velocity,
    rule_impossible_travel
]