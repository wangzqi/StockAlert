## Running Instructions
This folder contains the code to generate the input and send to Kinesis, and front end. Both of them run on the same AWS EC2 instance.

### EC2
* Spin up an EC2 instance (m4.large is used here). 
* Make sure that all the python and system requirements (in requirements.txt) are installed.
* Clone this repo to the EC2 node. 
* Go to StockAlert/src/ in your terminal.

#### Front End
* Type "chmod +x app.py".
* Type "python app.py".
* Go to the website that is specified. 

#### Input
* Type "chmod +x create-stream-input.py".
* Type "python create-stream-input.py".
