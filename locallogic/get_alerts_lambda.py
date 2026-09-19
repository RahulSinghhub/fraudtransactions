import boto3
import json
from decimal import Decimal


from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('fraud-transactions')

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def lambda_handler(event, context):
    # think through: how do you query the GSI specifically,
    # not the main table? boto3's table.query() has a parameter
    # for specifying which index to use.
    
    # you'll want to run this query TWICE - once for verdict='REVIEW',
    # once for verdict='BLOCK' - since a query only takes one partition
    # key value at a time. Combine both result lists.
    
    # return API Gateway's expected response shape:
    # {'statusCode': 200, 'headers': {...}, 'body': json.dumps(...)}


    review_response = table.query(IndexName = 'verdict-timestamp-index', 
                           KeyConditionExpression=Key('verdict').eq('REVIEW'))

    block_response = table.query(IndexName = 'verdict-timestamp-index',
                           KeyConditionExpression=Key('verdict').eq('BLOCK'))

    # Get the actual items
    review_alerts = review_response.get('Items', [])
    block_alerts = block_response.get('Items', [])

    # Combine both lists
    alerts = review_alerts + block_alerts

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(alerts, default=decimal_to_float)
    }