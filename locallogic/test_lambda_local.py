import json
import base64
from datetime import datetime
from lambda_function import lambda_handler

# Build a fake transaction, same as producer.py would send
txn_dict = {
    'txn_id': 'tl1',
    'account_id': 'A3',
    'amount': 500,
    'merchant_category': 'grocery',
    'city': 'Bengaluru',
    'timestamp': datetime.now().isoformat()
}

# Encode it exactly the way real Kinesis would present it to a Lambda
encoded_data = base64.b64encode(json.dumps(txn_dict).encode('utf-8')).decode('utf-8')

fake_event = {
    'Records': [
        {
            'kinesis': {
                'data': encoded_data,
                'partitionKey': 'A3'
            }
        }
    ]
}

lambda_handler(fake_event, None)