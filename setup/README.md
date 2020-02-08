## EC2 set up
m4.large


## Kinesis set up
Create a Kinesis stream with 20 shards: 

    python3 create-stream20.py
Register it

    aws kinesis register-stream-consumer --consumer-name con1 --stream-arn arn:aws:kinesis:us-east-1:503138534289:stream/RI1_fanout


### Kinesis
* Clone this repo to the your local machine or EC2 node. 
* Go to StockAlert/setup/.
* Create Kinesis Stream:

        python3 create-stream.py


### Lambda
* Spin up an EC2 instance (or cluster). 
* Make sure Spark is installed on all the instances.
* Make sure that all the python and system requirements (in requirements.txt) are installed.
* Clone this repo to the master EC2 node. 
* Go to InvisibleMe/src/.
* Edit user_input.py to the correct values. 
* Enter Spark-Submit run.py.

### Dynamodb
* Spin up an EC2 instance (or cluster). 
* Make sure Spark is installed on all the instances.
* Make sure that all the python and system requirements (in requirements.txt) are installed.
* Clone this repo to the master EC2 node. 
* Go to InvisibleMe/src/.
* Edit user_input.py to the correct values. 
* Enter Spark-Submit run.py.
