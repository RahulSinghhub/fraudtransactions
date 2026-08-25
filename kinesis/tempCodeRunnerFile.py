import boto3
import json
from dataclasses import asdict
from local_logic.transaction import Transaction
from datetime import datetime, timedelta



client = boto3.client('kinesis', region_name = 'ap-south-1')

for i in range(3):
    txn = Transaction(
        f"t{i+1}",
        "A1",
        100,
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