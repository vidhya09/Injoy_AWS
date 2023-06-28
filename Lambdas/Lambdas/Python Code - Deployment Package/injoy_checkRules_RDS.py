import json
import pymysql
import boto3
from datetime import datetime
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

    try:
        connection =pymysql.connect(host=endpoint, user=username, password=password, db=database_name)
        cursor =connection.cursor()
    
        eventid=event['event_id']
        username=event['username']
        num_participants=event['num_participants']
        total_p=int(num_participants)
        reg_allowed=True
        
        #Check if event with this eventID exists
        check=cursor.execute(f'''SELECT event_id FROM events WHERE EXISTS (SELECT event_id FROM events WHERE event_id='{eventid}')''')
        if(check>0):
            reg_allowed=True
        else:
            reg_allowed=False
            print("Event Does not exist, hence can't register.")
            return {
                "event_id":eventid,
                "num_participants":num_participants,
                "username":username,
                "reg_allowed":reg_allowed,
                "body":"Event Does not exist, hence can't register."
            }  
            
        #Check if time for registration has ended
        cursor.execute(f'''SELECT event_date FROM events WHERE event_id='{eventid}' ''')
        
        now=datetime.today().strftime('%Y-%m-%d')
        e_date=str(cursor.fetchone())
        e_date=e_date[15:-3]
        e_date=e_date.replace(" ","")
        formatting = "%Y,%m,%d"
        e_date=datetime.strptime(e_date, formatting)
        formatting = "%Y-%m-%d"
        now=datetime.strptime(now, formatting)
        print(e_date)
        print(now)
        if(now<=e_date):
            reg_allowed=True
        else:
            reg_allowed=False
            print("Event has ended, hence can't register.")
            return {
                "event_id":eventid,
                "num_participants":num_participants,
                "username":username,
                "reg_allowed":reg_allowed,
                "body":"Event has ended, hence can't register."
            }   
        
        #Check the participant count does not exceeds
        cursor.execute(f'''SELECT max_p FROM events WHERE event_id='{eventid}' ''')
        max_p=cursor.fetchone()
        max_p = int(''.join(map(str, max_p)))
        
        cursor.execute(f'''SELECT curr_p FROM events WHERE event_id='{eventid}' ''')
        curr=cursor.fetchone()
        curr= int(''.join(map(str,curr)))
        total_p+=curr
        
        if(total_p<=max_p):
            reg_allowed=True
            cursor.execute(f'''UPDATE events SET curr_p= {total_p} WHERE event_id='{eventid}' ''')
            connection.commit()
            print("Participant count(curr_p) updated")
        else:
            reg_allowed=False
            print("Participant count exceeded, hence can't register.")
            return {
                "event_id":eventid,
                "num_participants":num_participants,
                "username":username,
                "reg_allowed":reg_allowed,
                "body": "Participant count exceeded, hence can't register."
            }
        
        return {
            "event_id":eventid,
            "num_participants":num_participants,
            "username":username,
            "reg_allowed":reg_allowed
        }
    except:
        return{
            'body':'Error connecting to RDS'
        }