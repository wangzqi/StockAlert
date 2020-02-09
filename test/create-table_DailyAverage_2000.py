import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.create_table(
    TableName='DailyStockAverage2000',
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
        'ReadCapacityUnits': 2000,
        'WriteCapacityUnits': 2000
    }
)
table.meta.client.get_waiter('table_exists').wait(TableName='hashtags')
