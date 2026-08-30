from transaction import Transaction
from engine import FraudEngine
from datetime import datetime, timedelta

base_time = datetime(2026, 8, 15, 14, 0, 0)

fraud_engine = FraudEngine()

for i in range(5):
    txn = Transaction(
        f"t{i+1}",
        "A2",
        100,
        "test",
        "Bengaluru",
        base_time + timedelta(days=i)
    )


    result = fraud_engine.score(txn)

    print(
        result.txn_id,
        result.score,
        result.verdict,
        result.reasons
    )

txn6 = Transaction(
    "t6","A2", 100, "test", "DELHI", base_time + timedelta(minutes=5))

txn7 = Transaction(
    "t7","A2", 12200, "test", "Bengaluru", base_time + timedelta(minutes=5))

txn8 = Transaction(
    "t8","A2", 100, "test", "Bengaluru", base_time + timedelta(minutes=5))


result = fraud_engine.score(txn6)

print(
    result.txn_id,
    result.score,
    result.verdict,
    result.reasons
)