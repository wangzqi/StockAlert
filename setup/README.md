## EC2 set up
m4.large


## Tools set up
For tools setting up, 
* Clone this repo to the your local machine or EC2 node. 
* Go to StockAlert/setup/.

### Kinesis set up
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
