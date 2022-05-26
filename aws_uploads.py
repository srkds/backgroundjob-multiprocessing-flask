import boto3

def instantiate_boto_client():
    """
    Instantiates boto clinet
    """
    return boto3.client('s3')

def upload_files(file_name, bucket, object_name=None, args=None):
    """
    file_name: name of file on local comp
    bucket: bucketname
    object_name: name of file on s3
    """

    client = instantiate_boto_client()    
    object_name = "pyppeteer/" + "test2.pdf"
    
    response = client.upload_file(file_name, bucket, object_name, ExtraArgs = args)
    return "https://[BUCKET_NAME].s3.ap-south-1.amazonaws.com/pyppeteer/test2.pdf"