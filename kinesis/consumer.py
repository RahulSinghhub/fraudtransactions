import boto3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


client = boto3.client('kinesis', region_name = 'ap-south-1')

getdata = client.list_shards(StreamName='fraud-txn-stream')
print("SHARDS FOUND:", getdata['Shards'])   # <-- add this

for i in getdata['Shards']:
    resp = client.get_shard_iterator(StreamName='fraud-txn-stream', ShardId=i['ShardId'], ShardIteratorType='TRIM_HORIZON')
    
    result = client.get_records(
        ShardIterator=resp["ShardIterator"],
        Limit=10
    )
    print("RECORDS IN THIS SHARD:", len(result["Records"]))
    for record in result["Records"]:

        data = record["Data"].decode("utf-8")

        data = json.loads(data)

        print(data)

print("Done")
