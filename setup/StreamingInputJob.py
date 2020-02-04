import boto3
import csv
import json
import pandas as pd
from boto3.dynamodb.conditions import Key, Attr
import math
import time
from datetime import datetime, timedelta
#import s3fs
import os,sys
kinesis = boto3.client('kinesis', region_name='us-east-1')

import boto3

client = boto3.client('s3') 
resource = boto3.resource('s3') 
mybucket = resource.Bucket('stockalertinput') 

def StreamInput():

    while (datetime.now().second%5 != 0):
        time.sleep(0.001)

    EC2Timedelta = timedelta(hours=19)  # 19 hours is the time difference between EC2 and U.S. East timezone
    x2 = datetime.now()+EC2Timedelta
    if((x2.strftime("%H:%M:%S")>"16:00:00") or (x2.strftime("%H:%M:%S")<"09:30:00")):
        FileTime = datetime.strptime(datetime.now().strftime("%Y/%m/%d")+" 10:00:00","%Y/%m/%d %H:%M:%S")
        FileTimedelta=FileTime-datetime.now()-EC2Timedelta
    else:    
        FileTimedelta= timedelta(seconds=0)
    FileTime = datetime.now()+EC2Timedelta+FileTimedelta 
#    print(FileTime,datetime.now()+EC2Timedelta)

    while True:
#    for i in range(1):
        input = client.get_object(Bucket='stockalertinput', Key='Stocks_5s_sample_rate_'+FileTime.strftime("%H%M%S")+'.csv')
        input1 = pd.read_csv(input['Body'])
        Data = input1.to_json()
#        print(Data)

        while FileTime > datetime.now()+EC2Timedelta+FileTimedelta:
            time.sleep(1)
        print("Stock Market Time: ",FileTime," Time Now: ",datetime.now()+EC2Timedelta)
        response = kinesis.put_records(
            Records=[{'Data': Data,'PartitionKey': 'string'},],
            StreamName='RI1_fanout'
            )
        FileTime = FileTime + timedelta(seconds=5)


def main():
    StreamInput()

if __name__ == '__main__':
    main()
