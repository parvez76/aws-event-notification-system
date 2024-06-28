# Real-Time S3 Event Notification System with AWS Lambda and SNS

## Overview

This project showcases a robust and scalable AWS infrastructure that sends real-time email notifications for any changes in your S3 bucket using AWS Lambda and Amazon SNS. 

## Prerequisites

- Access to the AWS Console
- A valid email address

## Steps

### Step 1: Create an S3 Bucket

1. Login to the AWS console and open S3.
2. Create a bucket named "my-bucket".
3. Keep all settings as defaults and click on "Create bucket".

### Step 2: Set Up SNS (Simple Notification Service)

1. Go to the AWS console search and search for Simple Notification Service (SNS).
2. Open SNS and click on the "Create topic" option in the top left.
3. Give a name for the topic (e.g., mytopic) and click on "Next step".
4. Choose the "Standard" option and then click on "Create topic".
5. After the topic is created, create a subscription:
   - Click on "Create subscription" on the same page.
   - Leave the ARN as it is and select "Email" from the protocol options.
   - Enter your desired email in the endpoint section.
   - Click on "Create subscription".
6. Check your email for an AWS Notifications - Subscription confirmation email and click on "Confirm Subscription".

### Step 3: Create an IAM Policy

1. Go to the AWS console search and search for IAM.
2. In the IAM page, under the Access Management section, find and open "Policies".
3. Click on "Create policy".
4. Select the JSON format for the policy editor.
5. Remove all the existing JSON content and replace it with the following content:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "logs:DisassociateKmsKey",
                    "logs:DeleteSubscriptionFilter",
                    "logs:UntagLogGroup",
                    "logs:DeleteLogGroup",
                    "logs:DeleteLogStream",
                    "logs:PutLogEvents",
                    "logs:CreateExportTask",
                    "logs:PutMetricFilter",
                    "s3:GetObject",
                    "logs:CreateLogStream",
                    "logs:DeleteMetricFilter",
                    "logs:TagLogGroup",
                    "sns:Publish",
                    "logs:DeleteRetentionPolicy",
                    "logs:AssociateKmsKey",
                    "logs:PutSubscriptionFilter",
                    "logs:PutRetentionPolicy"
                ],
                "Resource": [
                    "arn:aws:logs:*:<your-aws-id>:log-group:*:log-stream:*",
                    "arn:aws:logs:*:<your-aws-id>:log-group:*",
                    "arn:aws:s3:::<your-s3-bucket-name>/*",
                    "arn:aws:sns:*:<your-aws-id>:<your-sns-topic-name>"
                ]
            }
        ]
    }
    ```

6. Update the AWS account ID, bucket name, and SNS topic name in the Resource section of the policy.
7. Click on "Next", review your policy, give it a name (e.g., mypolicy), and add a description.
8. Click on "Create policy".

### Step 4: Create an IAM Role

1. Go back to the IAM homepage and open "Roles" from the Access Management section.
2. Click on "Create role" and select "AWS service" as the entity type.
3. Select "Lambda" in the use cases section.
4. Click on "Next" and add the policy you created earlier (mypolicy).
5. Give the role a name (e.g., triggered-role) and click on "Create role".

### Step 5: Create a Lambda Function

1. Search for Lambda in the AWS console and open it.
2. Click on "Create function".
3. Select "Author from scratch", give a function name, and choose Python as the runtime.
4. Expand "Change default execution role" and choose "Use an existing role". Select the role created earlier (triggered-role).
5. Click on "Create function".
6. On the code and configuration page, replace the default code with the following content:

    ```python
    import json
    import boto3

    print('Loading function')

    s3 = boto3.client('s3')
    sns = boto3.client('sns')

    def lambda_handler(event, context):
        # Print received event
        print("Received event: " + json.dumps(event, indent=2))

        # Get bucket name, key, and event name from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        eventName = event['Records'][0]['eventName']

        try:
            # Get the object from the event
            response = s3.get_object(Bucket=bucket, Key=key)
            content_type = response['ContentType']
            print("Content Type: " + content_type)

            sns_message = (
                f"This email is sent to you as a file status has been changed in your bucket.\n\n"
                f"Bucket Name: {bucket}\n"
                f"File Name: {key}\n"
                f"Event Name: {eventName}\n"
                f"Content Type: {content_type}\n"
            )

            # Publish a message to the SNS topic
            response = sns.publish(
                TargetArn='arn:aws:sns:your-region:your-account-id:your-sns-topic-name',  # Update with your SNS topic ARN
                Message=sns_message,
                Subject='S3 Bucket Notification'
            )
            print(f"Message sent to SNS topic, response: {response}")

        except Exception as e:
            print(f"Error getting object {key} from bucket {bucket}. Event name: {eventName}. Error: {str(e)}")

        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent successfully')
        }
    ```

7. Update the `TargetArn` with the actual ARN of your SNS topic.
8. Click on "Deploy" to save the changes.

### Step 6: Add a Trigger to the Lambda Function

1. On the Lambda function page, click on "Add trigger".
2. Select S3 as the trigger and choose the bucket name created earlier.
3. Acknowledge the statement and click on "Add".

### Step 7: Add a Destination to the Lambda Function

1. Click on "Add destination" from the Lambda function page.
2. Select "On success" as the condition.
3. Choose your SNS topic ARN from the Destination section.
4. Click on "Save".

## Testing the Setup

1. Go to your S3 bucket and upload any object.
2. You should receive an email notification immediately after uploading.

## Congrats! Your Real-Time S3 Event Notification System with AWS Lambda and SNS setup is now complete.

