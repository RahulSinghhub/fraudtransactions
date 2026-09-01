import json

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

    @classmethod
    def from_json(cls, json_str:str)-> 'Transaction':
        data = json.loads(json_str)
        return cls(
            txn_id=data['txn_id'],
            account_id=data['account_id'],
            amount=data['amount'],
            merchant_category=data['merchant_category'],
            city=data['city'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )