import boto3
from s3folder import s3func
def create_dynamodb_table(event_id):
    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')
   
    # Define the table name and attributes
    table_name = event_id
    attribute_definitions = [
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        }
    ]
   
    # Define the primary key schema
    key_schema = [
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'
        }
    ]
   
    # Define the provisioned throughput
    provisioned_throughput = {
        'ReadCapacityUnits': 3,
        'WriteCapacityUnits': 3
    }
    
    try:
        # Create the DynamoDB table
        response = dynamodb.create_table(
            TableName=table_name,
            AttributeDefinitions=attribute_definitions,
            KeySchema=key_schema,
            ProvisionedThroughput=provisioned_throughput
        )
       
        # Wait for the table to be created
        # dynamodb.get_waiter('table_exists').wait(TableName=table_name)
       
        # Print the response
        print(response)
    except:
        return{
            'body':'Error creating event table in DynamoDB'
        }

def lambda_handler(event, context):
    
    event_id=event['event_id']
    eventname=event['event_name']
    e_venue=event['venue']
    eventhost=event['event_host']
    e_price=event['price']
    max_p=event['max_p']
    curr_p=event['curr_p']
    event_date=event['event_date']
    exist=event['exist']
    
    #Call Create table function
    create_dynamodb_table(event_id)
    
    #Call create event folder in s3 function
    s3func(event_id)
    
    return {
        "event_id":event_id,
        "event_name":eventname,
        "venue":e_venue,
        "event_host":eventhost,
        "price":e_price,
        "max_p":max_p,
        "curr_p":curr_p,
        "event_date":event_date,
        "exist":exist
        
    }