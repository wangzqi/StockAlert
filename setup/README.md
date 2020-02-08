## EC2 set up
m4.large


## Tools set up
For tools setting up, 
* Clone this repo to the your local machine or EC2 node. 
* Go to StockAlert/setup/.

### Kinesis
* Create Kinesis Stream:

        python3 create-kinesis-stream.py

### Lambda
* Go to AWS account -> lambda -> Functions
* Click Create function -> Author from scratch
* Copy the content in lambda-function-kinesis-consume.py to the Lambda function code
* Click "Add trigger" in the Designer portion and set up the Kinesis created above as the trigger: 
  
  Use Latest for "Starting position"

### Dynamodb
* Create Dynamodb table:

        python3 create-dynamodb-table.py
