import boto3

def create_api_gateway(api_name):
    apigateway = boto3.client('apigatewayv2')

    api_response = apigateway.create_api(
        Name=api_name,
        ProtocolType='HTTP'
    )

    api_id = api_response['ApiId']
    print(f"API created with ID {api_id}")
    return api_id

def create_routes(api_id, lambda_arn):
    apigateway = boto3.client('apigatewayv2')

    # Create POST /create-vpc route
    post_route = apigateway.create_route(
        ApiId=api_id,
        RouteKey='POST /create-vpc',
        Target=f"integrations/{lambda_arn}"
    )
    print(f"Created route POST /create-vpc: {post_route['RouteId']}")

    # Create GET /vpc-info route
    get_route = apigateway.create_route(
        ApiId=api_id,
        RouteKey='GET /vpc-info',
        Target=f"integrations/{lambda_arn}"
    )
    print(f"Created route GET /vpc-info: {get_route['RouteId']}")

def create_api(api_name, lambda_arn):
    api_id = create_api_gateway(api_name)
    create_routes(api_id, lambda_arn)
    return api_id

if __name__ == "__main__":
    lambda_arn = "<lambda_function_arn>"  # Replace with your Lambda function ARN
    api_id = create_api("VPC-API", lambda_arn)
    print(f"API created with ID {api_id}")
