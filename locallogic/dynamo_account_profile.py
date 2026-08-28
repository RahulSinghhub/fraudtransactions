import boto3
from datetime import datetime
from transaction import Transaction


class DynamoAccountProfile:
    def __init__(self, table_name= 'fraud-transactions', region_name = 'ap-south-1'):
        dynamodb = boto3.resource('dynamodb', region_name = region_name)
        self.tablename = dynamodb.Table(table_name)
    

    def record(self, txn: Transaction):
        self.tablename.put_item(Item = {
            'account_id': txn.account_id,
            'timestamp': txn.timestamp.isoformat(),
            'amount': txn.amount,
            'city': txn.city
        })

    def _get_recent(self, account_id, limit=20):
        response = self.tablename.query(
             KeyConditionExpression =  boto3.dynamodb.conditions.Key('account_id').eq(account_id),
             ScanIndexForward = False,
             Limit = limit)
        return response['Items']

    def average_amount(self, account_id):
        response =self._get_recent(account_id)
        total = sum(float(item['amount']) for item in response)
        return total / len(response) if response else 0

    def transactions_in_last(self, account_id, minutes, now):
        response =self._get_recent(account_id, 20)
        lst_to_add = []
        for item in response:
            ts = datetime.fromisoformat(item['timestamp'])
            if ((now- ts).total_seconds() / 60) <= minutes:
                lst_to_add.append(item)
        return lst_to_add

    def last_known_location(self, account_id):
        response = self._get_recent(account_id, 1)
        if response:
            item = response[0]
            return (item['city'], datetime.fromisoformat(item['timestamp']))
        return None