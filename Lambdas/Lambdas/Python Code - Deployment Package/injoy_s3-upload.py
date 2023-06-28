import json
import boto3
import base64
def lambda_handler(event, context):

    s3=boto3.client('s3')
    
    bucket = "injoy"
    folder = "portfolio/allimages"
    rs3 = boto3.resource("s3") 
    s3_bucket = rs3.Bucket(bucket)
    
    #Get image
    get_file_content= event["body"]
    decode_content= base64.b64decode(get_file_content)
    
    #counter to count all images
    files_in_s3 = [f.key.split(folder + "/")[1] for f in s3_bucket.objects.filter(Prefix=folder).all()]
    ctr=len(files_in_s3)
    key="portfolio/allimages/img"+str(ctr)+".jpeg"
    try:
        s3_upload=s3.put_object(Bucket="injoy",Key=key,Body=decode_content)
        if ctr>10:
            ctr=ctr%10
            if ctr==0:
                ctr=10
        key="portfolio/images/img"+str(ctr)+".jpeg"
        s3_upload=s3.put_object(Bucket="injoy",Key=key,Body=decode_content)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Uploaded!'),
            'link':'https://injoy.s3.amazonaws.com/portfolio/gallery.html'
        }
    except:
        return{
            'body':'Error uploading image to S3 bucket'
        }
        
