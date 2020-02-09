import boto3

client = boto3.client('kinesis')
response = client.create_stream(
   StreamName='RI30_fanout',
   ShardCount=30
)
