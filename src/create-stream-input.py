mport boto3
import pandas as pd
import math
import time
from datetime import datetime, timedelta

kinesis = boto3.client('kinesis', region_name='us-east-1')
client = boto3.client('s3')
resource = boto3.resource('s3')
mybucket = resource.Bucket('stockalertinput')
NumberOfShard = 30

def StreamInput():

    while (datetime.now().second%5 != 0):
        time.sleep(0.001)

    EC2Timedelta = timedelta(hours=19)  # 19 hours is the time difference between EC2 and U.S. East timezone
    x2 = datetime.now()+EC2Timedelta

    # For testing and demo purpose, we will use data starting from 10am if stock market is closed.
    if((x2.strftime("%H:%M:%S")>"16:00:00") or (x2.strftime("%H:%M:%S")<"09:30:00")):
        FileTime = datetime.strptime(datetime.now().strftime("%Y/%m/%d")+" 10:00:00","%Y/%m/%d %H:%M:%S")
        FileTimedelta=FileTime-datetime.now()-EC2Timedelta
    else:
        FileTimedelta= timedelta(seconds=0)
    FileTime = datetime.now()+EC2Timedelta+FileTimedelta

    while True:
        s3file = client.get_object(Bucket='stockalertinput', Key='Stocks_5s_sample_rate_'+FileTime.strftime("%H%M%S")+'.csv')
        input = pd.read_csv(s3file['Body'])
        while FileTime > datetime.now()+EC2Timedelta+FileTimedelta:
            time.sleep(1)
        print("Stock Market Time: ",FileTime," Time Now: ",datetime.now()+EC2Timedelta)

        record_per_shard = math.ceil(input['Stock'].count()/NumberOfShard)
        for i in range(NumberOfShard):
            rowstart = i*record_per_shard
            rowend = (i+1)*record_per_shard
            Data = input[rowstart:rowend].to_json()
            partitionkey = str(int(i*(2**128/NumberOfShard)))
            response = kinesis.put_records(
                    Records=[{'Data': Data,'ExplicitHashKey': partitionkey, 'PartitionKey':'partitionkey'},],
                    StreamName='RI30_fanout'
                )
        FileTime = FileTime + timedelta(seconds=5)

def main():
    StreamInput()

if __name__ == '__main__':
    main()
