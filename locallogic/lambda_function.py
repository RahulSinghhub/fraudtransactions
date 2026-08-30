import base64

from transaction import Transaction
from engine import FraudEngine

def lambda_handler(event, context):
    fraudengine = FraudEngine()
    for record in event['Records']:
        kinesis_data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        txn = Transaction.from_json(kinesis_data)
        result = fraudengine.score(txn)
        print(
            result.txn_id,
            result.score,
            result.verdict,
            result.reasons
        )


