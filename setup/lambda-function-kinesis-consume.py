from __future__ import print_function
import boto3
from datetime import datetime
import time
import base64, json, decimal

def lambda_handler(event, context):
    dynamo_db = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamo_db.Table('DailyStockAverage')

    for record in event['Records']:
        input = json.loads(base64.b64decode(record['kinesis']['data']))

        i=0
        for key in input['Time']:
            i=i+1
            TransactTime = input['Time'][key] 
            Stock = input['Stock'][key]
            Price  = decimal.Decimal(str(input['Price'][key]))
            Volume = input['Volume'][key]
            if i%150 == 0:
                print("Number of records processed: ",i," at time ",TransactTime)
                
            ItemExists = table.get_item(Key={'Stock':Stock})
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

