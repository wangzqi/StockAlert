import boto3

client = boto3.client('kinesis')
response = client.create_stream(
   StreamName='RI1_fanout',
   ShardCount=1
)
