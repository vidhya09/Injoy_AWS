import json
import boto3

def lambda_handler(event, context):
    # Extract the request body data

    #Access the relevant fields from the request body
    event_id = event['event_id']
    username = event['username']
    num_participants = event['num_participants']
    reg_allowed=event['reg_allowed']
    
    try:
        # Fetch the user details from Amazon Cognito
        user_pool_id = 'us-east-1_kyMBBm9VN'
        cognito_client = boto3.client('cognito-idp')
        response = cognito_client.admin_get_user(
            UserPoolId=user_pool_id,
            Username=username
        )
    
    # Extract the required user attributes from the Cognito response
    user_attributes = {}
    for attr in response['UserAttributes']:
        if attr['Name'] == 'email':
            user_attributes['email'] = attr['Value']
        elif attr['Name'] == 'phone_number':
            user_attributes['phone_number'] = attr['Value']
        elif attr['Name'] == 'gender':
            user_attributes['gender'] = attr['Value']
        elif attr['Name'] == 'name':
            user_attributes['name'] = attr['Value']
    except:
        return{
            'body':'Error retrieving details for the given username from Cognito'
        }
    
    try:
        # Add the user details to the DynamoDB table
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(event_id)
        item = {
            'username': username,
            'num_participants': num_participants,
            'email': user_attributes.get('email', ''),
            'phone_number': user_attributes.get('phone_number', ''),
            'gender': user_attributes.get('gender', ''),
            'name': user_attributes.get('name', '')
        }
        table.put_item(Item=item)
        return {
            'statusCode': 200,
            'reg_allowed':reg_allowed,
            'event_id':event_id,
            'username':username,
            'body': 'Thankyou for showing interest, your data is submitted successfully.'
        }
    except:
        return{
            'body':'Error adding user to DynamoDB'
        }