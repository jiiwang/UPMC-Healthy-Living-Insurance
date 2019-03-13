# UPMC-Healthy-Living-Insurance
A project of Cloud Computing

Here's the work flow/specification of our system.

When a food image is uploaded into an S3 bucket, a Lambda function will be triggerd which downloads the image, call Amazon Rekoginition API to get a label of this image in the form of <feature, confidence> and calculates a score for this image based on an algorithm. This lambda function will store scores in DynamoDB.

On the EC2 instance, a web application is built based on Flask framework. It allows user to view his diet scores. Data visualization tool called Highcharts.js is utilized. 

Thereafter, these evaluations can be used for UPMC to recommend best insurance plan for its customers accordingly. (This part is not implemented yet)
