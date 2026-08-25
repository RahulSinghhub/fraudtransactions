from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    txn_id: str
    account_id: str
    amount: float
    merchant_category: str
    city: str
    timestamp: datetime

    def hour_of_day(self) -> int:
        return self.timestamp.hour