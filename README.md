# AWSLexBackToPreviousQuestion

```bash
.
├── README.md                   <-- This instructions file
├── lambda_function             <-- Source code for a lambda function
│   ├── __init__.py
│   └── app.py                  <-- Lambda function code
└── template.yaml               <-- SAM template
```

## Deploy the Lex Chatbot 

Please use the excel file BackToPrevious.xlsx to create a test chatbot using ExcelLexBot (https://github.com/wongcyrus/ExcelLexBot) .

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
    --s3-bucket BUCKET_NAME
```

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name AWSLexBackToPreviousQuestion \
    --capabilities CAPABILITY_IAM
```
