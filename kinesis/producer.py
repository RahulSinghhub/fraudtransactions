import boto3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dataclasses import asdict
from locallogic.transaction import Transaction
from datetime import datetime, timedelta

client = boto3.client('kinesis', region_name = 'ap-south-1')

for i in range(4):
    txn = Transaction(
        f"t{i+1}",
        "A5",
        600,
        "test",
        "Bengaluru",
        datetime.now() + timedelta(days = i)
    )



    txn_data = asdict(txn)
    txn_data["timestamp"] = txn.timestamp.isoformat()

    result = json.dumps(txn_data).encode("utf-8")

    response = client.put_record(StreamName = 'fraud-txn-stream', Data = result, PartitionKey = txn.account_id)

    print(response['SequenceNumber'])
    print(response['ShardId'])

txn = Transaction(
        f"t{i+1}",
        "A5",
        600,
        "test",
        "allahabad",
        datetime.now() + timedelta(days = i)
    )

txn_data = asdict(txn)
txn_data["timestamp"] = txn.timestamp.isoformat()
result = json.dumps(txn_data).encode("utf-8")
response = client.put_record(StreamName = 'fraud-txn-stream', Data = result, PartitionKey = txn.account_id)
print(response['SequenceNumber'])
print(response['ShardId'])