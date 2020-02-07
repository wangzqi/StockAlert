# StockAlert
Justin Wang's Insight-BOSTON-20A Data Engineering Project

## Table of Contents
1. [Problem](README.md#problem)
1. [Basic Strategy](README.md#basic-strategy)
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


## Basic Strategy

![Pipeline](docs/pipeline.png)

The strategy was to allow the user to input **beginning file location**, **write location**, **columns** to be encrypted (or decrypted), whether you want it **encrypted** or **decrypted**, and the **delimiter** separating data on a Flask front end. This is then fed into a Spark program which pulls the correct file, distributes it across multiple nodes, encrypts the information on each node, then returns it back to the main node. From here, the *newly encrypted* file is written back into the EC2 container and the key for the encryption is stored in my personal EC2 bucket. An illustration of my chosen pipeline can be shown above. 

For a majority of the testing of my code, I used [FEC Donation Data](https://www.fec.gov/data/browse-data/?tab=bulk-data) and [White Pages](http://www.odditysoftware.com/download_databases/29_white-pages-data_1.html). 

## Running Instructions
### Main Method
* Spin up an EC2 instance (or cluster). 
* Make sure Spark is installed on all the instances.
* Make sure that all the python and system requirements (in requirements.txt) are installed.
* Clone this repo to the master EC2 node. 
* Go to InvisibleMe/tools/ in your terminal.
* Type "chmod +x front_end.py".
* Type "python front_end.py".
* Go to the website that is specified. 
* Enter the information as prompted. 
* Hit Submit. 

### Secondary Method
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


## Files in Repo 

### column_operations.py

#### description: 
This file has just one function, **cleaning_data**. This function takes in a row and based on whether it was specified that a particular column should be *encrypted* or *decrypted*, it performs this operation on that column but leaves the rest of the column untouched. This is returned in the format of Row(key1 = value1, key2 = value2, ...) where the keys are merely the column names (assumed to be 1, 2, 3, 4,... unless otherwise specified).    


### creating_keys.py

#### description: 
This file contains three functions. **creating_a_key** simply takes a pre-specified list (called *qwerty_list* through this program) and returns a random sampling (with replacement) of 16 of these elements and returns a string of them. 
The next function, **creating_dict_of_keys** simply employs **creating_a_key** 2n times (where n is the number of columns to be encrypted) and stores this information in a dictionary where the schema is column_id = (key, initial_vector). This allows for each column to have a unique key in order to increase the security of the information. 
The final function, **making_key_dict** takes the specification of *encryption* or *decryption* and creates the appropriate key dictionary, either by pulling a previously saved dictionary (see the descryption in Basic Strategy) or by creating a new one by calling **creating_dict_of_keys**. 
The bottom of this file then specifies two variables which will be used throughout, *key_dict* and *key_list*. Note that they key_list is just a list version of the key_dict. They are used for slightly different purposes through the function depending on which is faster/easier. 

### decryption.py

#### description: 
The only function is **decryption**. This simply takes a base64 message that has been encrypted using a specified key and initial vector, returns the object to a byte string, and then decodes the string. 

### encryption.py

#### description: 
The first function is **making_multiple_16**. This function exists because AES assumes the message length to be a multiple of 16. This function takes a string of any length and adds spaces at the end of it until the length of the string is a multiple of 16. Then it returns this string. 
The second function is **encryption**. This simply takes a string message, a key, and initial vector, encodes the string using AES, and then encodes it using base64. Then it returns this string. 

### user_input.py

#### description:
This file names universial variables that will be used through the program. It does this by referencing a file that has been created by the **front_end.py** in the current directory. One exception to this is the *keys_write_path*. This will always be my own personal S3 bucket for sake of security. 

### run.py

#### description:
This is the main run function and also where the pySpark is used. Everything is initiallized and then eventually run within this function. It has an if statement to deal with the fact that if I am encrypting (rather than decrypting), we need to write the keys to my S3. There is also a timer to keep an eye on how long it took for the function to run. 

### front_end.py

#### description:
This is where my Flask program is stored. It references various forms and .html files that are stored in their proper place. My hope is that their construction is self-evident, however, feel free to contact me with questions. 

## Encryption
For this project, I chose to employ the Rijndael Cypher, commonly known as AES (Advanced Encryption System). I chose this for three reasons, primarily: 
* it scales linearly (i.e. log(n))
* it provides a one-to-one mapping, given a key and name. That means that Samuel Judge and Herald Gerard will be encrypted uniquely, so they can still be seen as "person A" and "person B," for sake of research. 
* it is a symmetric code. That is to say, there is one unique key (and initial vector) that one person holds. This seemed an easier proposition than trying to put a secure, asymmetric key system into place. 

For more reading and detail on AES, please read this [article](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) or watch this [video](https://www.youtube.com/watch?v=liKXtikP9F0&t=644s). 

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
* [Samuel David Judge](https://www.linkedin.com/in/samueldjudge/)
* Samuel.D.Judge@gmail.com
* 269.921.0330
