# StockAlert
Justin Wang's Insight-BOSTON-20A Data Engineering Project

## Table of Contents
1. [Problem](README.md#problem)
1. [Pipeline](README.md#Pipeline)
1. [Running Instructions](README.md#running-instructions)
1. [Demo](README.md#demo)
1. [Assumptions](README.md#assumptions)
1. [Files in Repo](README.md#files-in-repo)
1. [Encryption](README.md#encryption)
1. [Scalability](README.md#scalability)
1. [Future Work](README.md#future-work)
1. [Contact Information](README.md#contact-information)

## Problem

A once-every-three-years study by the Federal Reserve Board found that in 2016, 51.9 percent of United States families owned stocks, either directly or as part of a fund. But most of them are fulltime workes and, at the same time, busy parents. There isn't much time for them to watch the market. Usually they are the ones got stuck when a crash happens. 

*Solution:* The goal of this program is to process real-time stock transaction information and alert users when stocks in their watchlists have big fluctuations.


## Pipeline

![Pipeline](docs/Pipeline.png)

* The input data is stored on Amazon S3.
* One Amazon EC2 instance is deployed to read and put records to Kinesis.
* The records streamed through Kinesis and triggered Lambda to process. 
* The output are stored on Dynamodb. 

## Running Instructions
### EC2
* Spin up an EC2 instance. 
* Make sure that all the python and system requirements (in requirements.txt) are installed.
* Clone this repo to the EC2 node. 
* Go to StockAlert/src/ in your terminal.

#### Front End
* Type "chmod +x app.py".
* Type "python app.py".
* Go to the website that is specified. 
* Hit Submit. 

#### Input
* Type "chmod +x app.py".
* Type "python app.py".
* Go to the website that is specified. 
* Hit Submit.

### Kinesis
* Spin up an EC2 instance (or cluster). 
* Make sure Spark is installed on all the instances.
* Make sure that all the python and system requirements (in requirements.txt) are installed.
* Clone this repo to the master EC2 node. 
* Go to InvisibleMe/src/.
* Edit user_input.py to the correct values. 
* Enter Spark-Submit run.py.

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

## Demo

[Here](https://youtu.be/KMAP3Op4jkI) you can see a video of my application in the works. 

In the first part, you can see an example of data that is stored in an S3 Bucket. Then you see the front end, where the information is inputted. Then the program is run and we return to the S3 Bucket to see that our information is now there. Once we look at it, we see that the columns that were specified have been encrypted. 

[Here](https://youtu.be/rsZm3JbHMSM) you can watch a video of my presentation where I discuss this project, along with my [slides](https://docs.google.com/presentation/d/1ZI-L-aVYDdLWXpPOYjrs-DwDfPyZH8OSLtSQ9Szt1EA/edit?usp=sharing). 


## Assumptions
* The columns to be encrypted **must be strings.** If they are a float, integer, dictionary, or list, the program will automatically change it to a string.
* If a value is empty, the program automatically fills that spot with "NULL." This is to avoid a bug in the built-in AES encryption service.
* I am assuming that the user is storing their information in an Amazon S3 bucket. 
* I am assuming that the information is relational and organized in a .csv type format, though the program does allow for flexibility as to what the delimiter is. 
* The assumption is that the *master* EC2 node has sufficient space to hold the data. This can be modified by writing to a MySQL database first, though the time cost is signficantly larger. 

## Scalability


The red dots on the plot represents four nodes and the black dots represents one node. The red and black line are the so-called "line of best fit" for the red and black points, respectively. We notice the definite increase in speed as we increase nodes, which shows a distribution. 

![Pipeline](docs/scalability.png)

We also note that this is linear. We **emphasize** that this is not shocking. This does not show anything in particular except that things are working *as expected*. 

## Future Work
While this program runs reasonably efficiently and distributes as expected, there are several improvements to be made. 
* Writing to an S3 Bucket is a pain. You cannot append to the end of an existing file in the bucket, which makes it impossible for all your nodes to simultaneously write to the same file. This led to having to push all the data into a single node causing a memory issue as 400G clearly overwhelmed it. 
The first solution I employed was to first write to a MySQL database before then copying that into an S3 Bucket. While this works, it caused a huge lag in time. To avoid creating a memory error, I used the following [pipeline](https://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/datapipeline-dg.pdf#dp-copydata-mysql). In the case of some smaller batches, this could create a nearly 2x increase in time. It is entirely possible that this could be corrected with more efficient code, but I had not figured it out before this submission. I will update if I do.  
The second solution I employed was the purchase a larger master node to handle the amount of data being fed into the system. This was significantly faster than the aforementioned around-about method, but it also came with a financial cost. 
Coming up with a good solution to this problem that can both maximize time and monetary costs is one of the next steps. 

* If I choose to buy bigger computers and more nodes, I wind up with a situation where most of these resources are not being used efficiently (or not used at all). I want to figure out how to gauge what I need when a project is submitted and not waste time/money on uneeded power. A clever implimentation of [Kubernetes](https://kubernetes.io/) would allow me to do this, since a majority of my work is embarrassingly-parallizable. However, given the limited time I was able to spend on this project, I was not able to test out this as much as I would like. 

* There are several asthetic things I would like to fix. For example, due to the lack of ordering on dictionaries, my columns can shuffle, depending on how I choose to store them. Certainly this is fixible, but I did not find a more beautiful solution yet. Additionally, the decryption is not completely user-friendly. The decryption is done by creating a unique key that is tagged to the encrypted file and I can use to locate the approrpiate key(s) for that file. 

## Contact Information
* Wangzqi@gmail.com
