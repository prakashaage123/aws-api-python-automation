import boto3

def create_s3_bucket(bucket_name):
    s3 = boto3.client('s3')
    response = s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': 'us-east-1'}
    )
    return response['Location']

if __name__ == "__main__":
    bucket_name = "<unique_bucket_name>"
    bucket_location = create_s3_bucket(bucket_name)
    print(f"S3 bucket created at location {bucket_location}")
