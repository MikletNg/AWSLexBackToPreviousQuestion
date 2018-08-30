# AWSLexBackToPreviousQuestion

```bash
.
├── README.md                   <-- This instructions file
├── lambda_function             <-- Source code for a lambda function
│   ├── __init__.py
│   └── app.py                  <-- Lambda function code
└── template.yaml               <-- SAM template
```
## Packaging and deployment

Firstly, we need a `S3 bucket` where we can upload our Lambda functions packaged as ZIP before we deploy anything - If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```bash
aws s3 mb s3://BUCKET_NAME
```

Next, run the following command to package our Lambda function to S3:

```bash
sam package \
    --template-file template.yaml \
    --output-template-file packaged.yaml \
    --s3-bucket wecarebillbucket
```

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name AWSLexBackToPreviousQuestion \
    --capabilities CAPABILITY_IAM
```

> **See [Serverless Application Model (SAM) HOWTO Guide](https://github.com/awslabs/serverless-application-model/blob/master/HOWTO.md) for more details in how to get started.**

After deployment is complete you can run the following command to retrieve the API Gateway Endpoint URL:

```bash
aws cloudformation describe-stacks \
    --stack-name AWSLexBackToPreviousQuestion \
    --query 'Stacks[].Outputs'
``` 