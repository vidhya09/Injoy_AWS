import pymysql
import json
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
    eventid=event['event_id']
    eventname=event['event_name']
    e_venue=event['venue']
    eventhost=event['event_host']
    e_price=event['price']
    max_p=event['max_p']
    curr_p=event['curr_p']
    event_date=event['event_date']
    database_name='injoy'
    
    # Connect to the RDS database
    try:
        conn = pymysql.connect(
            host=endpoint,
            user=username,
            password=password,
            database=database_name
        )
        print("Connected to RDS database.")
    except pymysql.Error as e:
        print("Error connecting to RDS database:", e)
        return {
            'statusCode': 500,
            'body': 'Error connecting to RDS database'
        }
    
    # SQL query to retrieve data from the RDS database
    query = f'''UPDATE events SET event_name = '{eventname}',event_venue = '{e_venue}',event_host ='{eventhost}',price ={e_price},max_p ={max_p},curr_p ={curr_p},event_date ='{event_date}' WHERE event_id ='{eventid}' '''
    
    # Execute the query
    try:
        cursor = conn.cursor()
        #Check if event with this eventID exists
        check=cursor.execute(f'''SELECT event_id FROM events WHERE EXISTS (SELECT event_id FROM events WHERE event_id='{eventid}')''')
        if(check<=0):
            reg_allowed=False
            print("Event Does not exist, hence can't register.")
            return {
                "statusCode":404,
                "body":"Event does not exist."
            }   
        
        cursor.execute(query)
        conn.commit()
    except pymysql.Error as e:
        print("Error executing query:", e)
        conn.close()
        return {
            'statusCode': 500,
            'body': 'Error executing query'
        }

    # Close the database connection
    conn.close()
    print("Closed RDS connection.")

    # Return the processed data or any desired response
    return {
        'statusCode': 200,
        'body':'Event is updated successfully!'
    }
