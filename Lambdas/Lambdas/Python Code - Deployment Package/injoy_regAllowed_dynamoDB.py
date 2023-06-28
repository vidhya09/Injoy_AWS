import boto3
import json


dynamodb = boto3.client('dynamodb')
def lambda_handler(event, context):
    # Retrieve details from the event
    eventid=event['event_id']
    username=event['username']
    num_participants=event['num_participants']
    
    # Create a DynamoDB client
    
    try:
        #Check if table exists else not allowed
        response = dynamodb.list_tables()
        if eventid not in response['TableNames']:
            return {
                'statusCode': 200,
                "event_id":eventid,
                "username":username,
                "reg_allowed":False,
                'body': 'Table does not exist.'
            }
        # Get item using the partition key
        response = dynamodb.get_item(
            TableName=eventid,
            Key={
                'username':{'S': username}
            }
        )
        
        # Check if user has already registered
        if 'Item' in response:
            return {
                'statusCode': 200,
                "event_id":eventid,
                "username":username,
                "reg_allowed":False,
                "body":"User Already registered"
            }
        
        else:
            return {
                'statusCode': 200,
                "event_id":eventid,
                "num_participants":num_participants,
                "username":username,
                "reg_allowed":True
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}'
        }
