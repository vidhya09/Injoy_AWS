import boto3
# Create folder with name as eventid in S3
# Not implemented in project
def lambda_handler(event, context):
    # Extract the event ID from the input event
    event_id = event['event_id']
    
    # # Extract the image file from the form data
    # image_file = event['image']
    
    # Create the folder in the S3 bucket
    s3 = boto3.client('s3')
    bucket_name = 'injoy'
    folder_name = event_id + '/'
    s3.put_object(Body='', Bucket=bucket_name, Key=folder_name)
    
    # Upload the image to the folder in the S3 bucket
    key = folder_name + image_file.filename
    s3.upload_fileobj(image_file.file, bucket_name, key)
    
    # Return a response indicating the successful image upload
    response = {
        'event_id': event_id
    }
    
    return response
