## EC2 set up
m4.large


## Kinesis set up
Create a Kinesis stream with 20 shards: 
    python3 create-stream20.py
Register it
    aws kinesis register-stream-consumer --consumer-name con1 --stream-arn arn:aws:kinesis:us-east-1:503138534289:stream/RI1_fanout
