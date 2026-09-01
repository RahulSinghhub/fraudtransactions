from collections import defaultdict, deque
from datetime import timedelta
from transaction import Transaction


class AccountProfile:
    def __init__(self, history_size: int = 20):
        self.history = defaultdict(lambda: deque(maxlen=history_size))
        self.last_location = {}

    def record(self, txn: Transaction):
        self.history[txn.account_id].append(txn)
        self.last_location[txn.account_id] = (txn.city, txn.timestamp)

    def average_amount(self, account_id: str) -> float:
        past = self.history[account_id]
        if not past:
            return 0.0
        return sum(t.amount for t in past) / len(past)

    def transactions_in_last(self, account_id: str, minutes: int, now):
        window_start = now - timedelta(minutes=minutes)
        return [t for t in self.history[account_id] if t.timestamp >= window_start]

    def last_known_location(self, account_id: str):
        return self.last_location.get(account_id)