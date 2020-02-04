from __future__ import print_function
import boto3
#import datetime 
from datetime import datetime
import time


import base64
import json
import decimal



def lambda_handler(event, context):
#    print('Lambda Loading function')


    dynamo_db = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamo_db.Table('DailyStockAverage')

    kinesis = boto3.client('kinesis')
    shard_id = 'shardId-000000000000'
    pre_shard_it = kinesis.get_shard_iterator(StreamName='RI1_fanout', ShardId=shard_id, ShardIteratorType='LATEST')
    shard_it = pre_shard_it ['ShardIterator']
    
    time.sleep(5)
    out = kinesis.get_records(ShardIterator=shard_it, Limit=10)
    print("Get records finished time")

    for record in out['Records']:
#        print("Justin Read records",record['Data'])
        input=json.loads(record['Data'])
#        print(input)

        i=0
        for key in input['Time']:
            i=i+1
            if i<=9000:
                TransactTime = input['Time'][key] 
                Stock = input['Stock'][key]
                Price  = decimal.Decimal(str(input['Price'][key]))
                Volume = input['Volume'][key]

            
                if i%500 == 0:
                    print("Number of records processed: ",i," at time ",TransactTime)
                
             

#            print(TransactTime,Stock,Price,Volume)
                ItemExists = table.get_item(Key={'Stock':Stock})
#            print(ItemExists)
                if 'Item' in ItemExists:
                    if Price < 1:
                        DailyAveragePrice = decimal.Decimal(round((ItemExists['Item']['DailyAveragePrice'] * ItemExists['Item']['TotalVolume'] \
                                            + Price * Volume)/(ItemExists['Item']['TotalVolume']+Volume),4))
                    else:
                        DailyAveragePrice = decimal.Decimal(round((ItemExists['Item']['DailyAveragePrice'] * ItemExists['Item']['TotalVolume'] \
                                            + Price * Volume)/(ItemExists['Item']['TotalVolume']+Volume),2))
                    TotalVolume = ItemExists['Item']['TotalVolume']+Volume
                    Percentage = decimal.Decimal(round((Price-DailyAveragePrice)/DailyAveragePrice,4))
                    response = table.update_item(
                        Key={'Stock':Stock},
                        UpdateExpression="set DailyAveragePrice=:val1, Price=:val2, TotalVolume=:val3, Percentage=:val4, TransactTime=:val5",
                        ExpressionAttributeValues={':val5': TransactTime,':val1': DailyAveragePrice,':val2':Price, ':val3':TotalVolume, ':val4':Percentage},
                        ReturnValues="UPDATED_NEW"
                    )
                else:
                    response = table.put_item(
                        Item={'Stock':Stock, 'TransactTime':TransactTime,'DailyAveragePrice':Price, 'Price':Price, 'TotalVolume':Volume,'Percentage':0}

                    )
