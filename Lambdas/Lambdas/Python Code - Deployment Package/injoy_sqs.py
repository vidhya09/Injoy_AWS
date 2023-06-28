import boto3

def lambda_handler(event, context):
    
    # Create an SQS client
    sqs = boto3.client('sqs')
    
    # Specify the URL of your SQS queue
    queue_url = 'https://sqs.us-east-1.amazonaws.com/365472796140/injoy-sqs'
    event_id = event['event_id']
    
    # Create a message with the event details
    exist=event['exist']
    if(exist==True):
        message=f"Hello Admin!\n\nA new event with event ID :{event_id} was not created as it already exists."
        sqs.send_message(QueueUrl=queue_url, MessageBody=message)
        return{
            'statusCode':200,
            'body':'Event was not created as it already exists'
        }
    event_name = event['event_name']
    venue = event['venue']
    event_host=event['event_host']
    price=event['price']
    max_p=event['max_p']
    curr_p=event['curr_p']
    event_date=event['event_date']
    message = f"Hello Admin!\n\nA new event:{event_name} was created successfully.\n\nHere are the details:\nEvent ID: {event_id}\nName: {event_name}\nDate: {event_date}\nMaximum Participants: {max_p}\nVenue: {venue}\nFee:{price}"
    
    # sqs_waiter=sqs.get_waiter('sqs_waiter')
    # sqs_waiter.wait(QueueUrl=queue_url)
    # Send the message to the SQS queue'
    try:
        sqs.send_message(QueueUrl=queue_url, MessageBody=message)
        return {
            'statusCode': 200,
            'body': 'Event details added to SQS queue successfully'
        }
    except:
        return{
            'body':'Error sending the message to SQS queue
        }