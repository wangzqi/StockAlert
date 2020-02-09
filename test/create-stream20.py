import boto3

client = boto3.client('kinesis')
response = client.create_stream(
   StreamName='RI20_fanout',
   ShardCount=20
)
