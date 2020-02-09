# StockAlert
Justin Wang's Insight-BOSTON-20A Data Engineering Project

## Table of Contents
1. [Problem](README.md#problem)
1. [Pipeline](README.md#Pipeline)
1. [Running Instructions](README.md#running-instructions)
1. [Demo](README.md#demo)
1. [Files in Repo](README.md#files-in-repo)
1. [Engineering Challenges](README.md#Engineering-Challenges)
1. [Contact Information](README.md#contact-information)

## Problem

A once-every-three-years study by the Federal Reserve Board found that in 2016, 51.9 percent of United States families owned stocks, either directly or as part of a fund. But most of them are fulltime workers and, at the same time, busy parents. There isn't much time for them to watch the market. Usually they are the ones got stuck when a crash happens. 

*Solution:* The goal of this program is to process real-time stock transaction information and alert users when stocks in their watchlists have big fluctuations.


## Pipeline

![Pipeline](docs/Pipeline.png)

* The input data is stored on Amazon S3.
* One Amazon EC2 instance is deployed to read and put records to Kinesis.
* The records streamed through Kinesis and triggered Lambda to process. 
* The output are stored on Dynamodb. 


## Demo

[Here](https://docs.google.com/presentation/d/1Hfd_69M8oH_Z5qKHjjJgYDO-kT6uJuBI7YAezgpVQqw/edit) you can see a demo of my application in the works. 

## Engineering Challenges
Latency - Solution: Fan-out problem with creating multiple shards.

Cost - Solution: Optimize the setup and make sure there is no short stave.

## Contact Information
* Wangzqi@gmail.com
