import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(
    TableName='DailyStockAverage1000',
    KeySchema=[
        {
            'AttributeName': 'Stock',
            'KeyType': 'HASH'
               
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'Stock',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1000,
        'WriteCapacityUnits': 1000
    }
)
table.meta.client.get_waiter('table_exists').wait(TableName='hashtags')
