# UPMC-Healthy-Living-Insurance
A project of Cloud Computing

When a food image is uploaded into an S3 bucket, a Lambda function will be trigged which will download the image,
call Amazon Rekoginition API to get <label, confidence> of this image and calculate a score for this image based on an algorithm.
This lambda function will store scores in DynamoDB.

On the EC2 instance, a web application is built based on Flask framework. It allows user to view his diet scores. Data visualization
tool called Highcharts.js is utilized. 
