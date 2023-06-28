import boto3

def lambda_handler(event, context):
    # Extract event details from the input event
    reg_allowed=event['reg_allowed']
    event_id = event['event_id']
    username=event['username']
    body=event['body']
    
    
    # Create an SQS client
    sqs = boto3.client('sqs')
    # Specify the URL of your SQS queue
    queue_url = 'https://sqs.us-east-1.amazonaws.com/365472796140/injoy-register-sqs'
    

    message=f"Hello,\nFor User: {username}\nFollowing details are received:\nEvent ID: {event_id}\nMessage: '{body}'"
    try:
        sqs.send_message(QueueUrl=queue_url, MessageBody=message)
        return{
            'statusCode':200,
            'body':'Message pushed to SQS queue.'
        }
    except:
        return{
            'body':'Error connecting to SQS'
        }
