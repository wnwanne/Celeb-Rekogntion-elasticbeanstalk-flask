# eb-flask
A flask web app that utlizes AWS services such as S3, Rekognition, Lambda, SQS, SNS, and DynamoDB to analyze a video input (particularly a current NBA celebrity interview) and return information about the celebrity. 

This was written very simplistically to utlize elastic beanstalk for an unmanaged deployment. 

The video upload triggers a lambda function that processes the video and stores the meta data in a DynamoDB table. The front end then queries that DynamoDB table to retireve info which it displays when the process is complete.
