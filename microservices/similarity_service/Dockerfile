FROM ubuntu:latest

RUN apt-get update

RUN pip install boto3  

ENTRYPOINT python run.py -q $SQS_QUEUE >> $LOG_FILE
