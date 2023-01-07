import boto3

def uploadFile(file_name,bucket_name,folder_name):

    # Set the access key and secret key
    access_key = "<access>"
    secret_key = "<secret>"

    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key)

    # Set the name of the bucket and the file to upload
    # bucket_name = 'do-reporting-test'
    # file_name = 'misspelled_words.csv'
    # folder_name = 'content'
    # Upload the file to S3
    s3.upload_file(file_name, bucket_name, "{0}/{1}".format(folder_name, file_name),ExtraArgs={'ACL': 'public-read'})

    print("file uploaded to s3 successfully")