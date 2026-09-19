### cmd to get arn's
aws dynamodb describe-table --table-name fraud-transactions --query "Table.TableArn"
aws kinesis describe-stream-summary --stream-name fraud-txn-stream --query "StreamDescriptionSummary.StreamARN"

aws dynamodb describe-table --table-name fraud-transactions --query "Table.TableArn"
aws kinesis describe-stream-summary --stream-name fraud-txn-stream --query "StreamDescriptionSummary.StreamARN"


### cmd to create sns
aws sns create-topic --name fraud-alerts

### cmd for subscribing to the email
aws sns subscribe --topic-arn arn:aws:sns:ap-south-1:563235961223:fraud-alerts --protocol email --notification-endpoint rrsmm152@gmail.com


### adding json for verdict and timestamp
aws dynamodb update-table --table-name fraud-transactions --attribute-definitions AttributeName=verdict,AttributeType=S AttributeName=timestamp,AttributeType=S --global-secondary-index-updates "[{\"Create\":{\"IndexName\":\"verdict-timestamp-index\",\"KeySchema\":[{\"AttributeName\":\"verdict\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"timestamp\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}}]"