## Running Instructions
This folder contains the code to generate the input and front end. Both of them run on the same AWS EC2 instance.

### EC2
* Spin up an EC2 instance (m4.large is used here). 
* Make sure that all the python and system requirements (in requirements.txt) are installed.
* Clone this repo to the EC2 node. 
* Go to StockAlert/src/ in your terminal.

#### Input

    $ chmod +x create-stream-input.py
    $ python3 create-stream-input.py

#### Front End
    $ chmod +x app.py
    $ python3 app.py
Go to the website that is specified. 

