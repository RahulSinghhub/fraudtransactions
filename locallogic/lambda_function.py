import base64
import boto3

from transaction import Transaction
from engine import FraudEngine

sns_client = boto3.client('sns', region_name='ap-south-1')


def lambda_handler(event, context):
    fraudengine = FraudEngine()
    for record in event['Records']:
        kinesis_data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        txn = Transaction.from_json(kinesis_data)
        result = fraudengine.score(txn)
        if result.verdict in ("REVIEW","BLOCK"):
            sns_client.publish(
                TopicArn = "arn:aws:sns:ap-south-1:563235961223:fraud-alerts",
                Message = f"Transaction {result.txn_id} flagged as {result.verdict} with score {result.score}. Reasons: {result.reasons}",
                Subject = f"Fraud Alert [{result.verdict}]: {result.txn_id}"
            )
        print(
            result.txn_id,
            result.score,
            result.verdict,
            result.reasons
        )


