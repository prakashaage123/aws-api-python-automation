
import boto3

def create_lambda_function(function_name, role_arn, handler):
    lambda_client = boto3.client('lambda')

    with open('lambda/lambda.zip', 'rb') as f:
        zipped_code = f.read()

    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.8',
        Role=role_arn,
        Handler=handler,
        Code={'ZipFile': zipped_code},
        Environment={
            'Variables': {
                'S3_BUCKET': '<your_s3_bucket_name>',
            }
        }
    )

    return response['FunctionArn']

if __name__ == "__main__":
    role_arn = "<iam_role_arn>"  
    function_arn = create_lambda_function('vpc-api-handler', role_arn, 'lambda_function.lambda_handler')
    print(f"Lambda function created with ARN {function_arn}")
