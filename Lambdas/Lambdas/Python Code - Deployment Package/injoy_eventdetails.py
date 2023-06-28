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
    query = "SELECT event_id, event_name, event_host, event_venue,price, max_p, curr_p FROM events"

    # Execute the query
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        print("Retrieved data from RDS:", results)
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
        'body':results
    }