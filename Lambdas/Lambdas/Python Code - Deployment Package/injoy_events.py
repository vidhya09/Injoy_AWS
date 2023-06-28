import json
import pymysql
import boto3

secretsmanager = boto3.client('secretsmanager', region_name='us-east-1')
def lambda_handler(event, context):
    
    secret_name = 'injoy_sm'
    response = secretsmanager.get_secret_value(SecretId=secret_name)

    # Parse the JSON string in the response
    secret = json.loads(response['SecretString'])

    # Retrieve the username and password from the secret
    username = secret['username']
    password = secret['password']
    endpoint=secret['host']
    
    # Extract the request body
    database_name='injoy'
    connection =pymysql.connect(host=endpoint, user=username, password=password, db=database_name)
    cursor =connection.cursor()
    eventid=event['event_id']
    eventname=event['event_name']
    e_venue=event['venue']
    eventhost=event['event_host']
    e_price=event['price']
    max_p=event['max_p']
    curr_p=event['curr_p']
    event_date=event['event_date']
    exist=False
    try:
        check=cursor.execute(f'''SELECT event_id FROM events WHERE EXISTS (SELECT event_id FROM events WHERE event_id='{eventid}')''')
        
        if(check>0):
            exist=True
            return{
                "exist":exist,
                "event_id":eventid
                }
        
        cursor.execute(f'''INSERT INTO events (event_id,event_name,event_venue,event_host,price,max_p,curr_p,event_date) VALUES('{eventid}','{eventname}','{e_venue}','{eventhost}',{e_price},{max_p},{curr_p},'{event_date}')''')
        connection.commit()
        
        return {
            "event_id":eventid,
            "event_name":eventname,
            "venue":e_venue,
            "event_host":eventhost,
            "price":e_price,
            "exist":exist,
            "max_p":max_p,
            "curr_p":curr_p,
            "event_date":event_date
        }
    except:
        return{
            'body':'Error adding and retrieving event details from RDS'
        }
    
