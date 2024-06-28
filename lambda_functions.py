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
