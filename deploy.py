
from python.create_vpc import create_vpc_and_subnets
from python.create_s3_bucket import create_s3_bucket
from python.create_lambda import create_lambda_function
from python.api_gateway import create_api

def deploy():
    print("🚀 Starting AWS Infrastructure Deployment...")

    # Step 1: Create VPC and Subnets
    print("📦 Creating VPC and Subnets...")
    vpc_id, subnet_ids = create_vpc_and_subnets()
    print(f"✅ VPC ID: {vpc_id}, Subnets: {subnet_ids}")

    # Step 2: Create S3 Bucket
    bucket_name = "<your_unique_bucket_name>"  # Replace with your bucket name
    print("📦 Creating S3 Bucket...")
    location = create_s3_bucket(bucket_name)
    print(f"✅ S3 Bucket created in {location}")

    # Step 3: Create Lambda Function
    function_name = "vpc-api-handler"
    role_arn = "<iam_role_arn>"  # Replace with your IAM role ARN
    handler = "lambda_function.lambda_handler"
    print("⚙️ Creating Lambda Function...")
    function_arn = create_lambda_function(function_name, role_arn, handler)
    print(f"✅ Lambda created with ARN: {function_arn}")

    # Step 4: Create API Gateway and integrate with Lambda
    api_name = "VPC-API"
    print("🌐 Creating API Gateway and Routes...")
    api_id = create_api(api_name, function_arn)
    print(f"✅ API Gateway created with ID: {api_id}")

    print("🎉 Deployment Completed Successfully!")

if __name__ == "__main__":
    deploy()
