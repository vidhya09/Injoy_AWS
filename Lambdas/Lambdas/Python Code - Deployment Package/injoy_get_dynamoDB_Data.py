import json
import boto3

def lambda_handler(event, context):
    tablename=event['event_id']
    dynamodb = boto3.client('dynamodb')
    
    try:
        #Check if table exists else not allowed
        response = dynamodb.list_tables()
        if tablename not in response['TableNames']:
            return {
                'statusCode': 200,
                'body': 'Table does not exist.'
            }
        
        client=boto3.resource("dynamodb")
        table=client.Table(tablename)
        response=table.scan()
        items=response["Items"]
        
        while 'LastEvaluatedKey' in response:
            # print(response['LastEvaluatedKey'])
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])
        l=[]
        for item in items:
            l.append(item)
        return {
            'statusCode': 200,
            'body': l
        }
    except:
        return{
            'body':'Error retrieving DynamoDB table '
        }