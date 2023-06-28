import boto3

def lambda_handler(event, context):
    # Create an SQS client
    sqs = boto3.client('sqs')
   
    # Specify the URL of your SQS queue
    queue_url = 'https://sqs.us-east-1.amazonaws.com/365472796140/injoy-register-sqs'
   
    try:
        # Retrieve the latest message from the SQS queue
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
        messages = response.get('Messages', [])
       
        # Check if there is a message in the queue
        if messages:
            message = messages[0]
            receipt_handle = message['ReceiptHandle']
            message_body = message['Body']
           
            # Publish the message to the SNS topic
            sns = boto3.client('sns')
            topic_arn = 'arn:aws:sns:us-east-1:365472796140:injoy-sns'
            sns.publish(TopicArn=topic_arn, Message=message_body)
           
            # Delete the message from the SQS queue
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
           
            return {
                'statusCode': 200,
                'body': 'Latest message retrieved from SQS, published to SNS, and deleted from SQS'
            }
        else:
            return {
                'statusCode': 200,
                'body': 'No messages found in the SQS queue'
            }
    except:
        return{
            'body':'Error retrieving messages from '
        }