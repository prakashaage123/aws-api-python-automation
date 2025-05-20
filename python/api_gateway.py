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

def create_lambda_integration(api_id, lambda_arn):
    apigateway = boto3.client('apigatewayv2')

    integration_response = apigateway.create_integration(
        ApiId=api_id,
        IntegrationType='AWS_PROXY',
        IntegrationUri=lambda_arn,
        PayloadFormatVersion='2.0',
        IntegrationMethod='POST'
    )

    integration_id = integration_response['IntegrationId']
    print(f"Lambda integration created with ID {integration_id}")
    return integration_id

def create_cognito_authorizer(api_id, user_pool_arn, user_pool_client_id):
    apigateway = boto3.client('apigatewayv2')

    authorizer_response = apigateway.create_authorizer(
        ApiId=api_id,
        AuthorizerType='JWT',
        IdentitySource=['$request.header.Authorization'],
        Name='CognitoAuthorizer',
        JwtConfiguration={
            'Audience': [user_pool_client_id],
            'Issuer': f'https://cognito-idp.<your-region>.amazonaws.com/{user_pool_arn.split("/")[-1]}'
        }
    )

    authorizer_id = authorizer_response['AuthorizerId']
    print(f"Cognito authorizer created with ID {authorizer_id}")
    return authorizer_id

def create_routes(api_id, integration_id, authorizer_id):
    apigateway = boto3.client('apigatewayv2')

    for route_key in ['POST /create-vpc', 'GET /vpc-info']:
        route_response = apigateway.create_route(
            ApiId=api_id,
            RouteKey=route_key,
            Target=f'integrations/{integration_id}',
            AuthorizationType='JWT',
            AuthorizerId=authorizer_id
        )
        print(f"Created route {route_key}: {route_response['RouteId']}")

def create_api_key_and_usage_plan(api_id):
    client = boto3.client('apigateway')

    # Create API key
    api_key_response = client.create_api_key(
        name='MyApiKey',
        enabled=True
    )
    api_key_id = api_key_response['id']
    print(f"API Key created: {api_key_id}")

    # Create usage plan
    usage_plan_response = client.create_usage_plan(
        name='MyUsagePlan',
        apiStages=[{
            'apiId': api_id,
            'stage': 'default'
        }],
        throttle={
            'rateLimit': 10,
            'burstLimit': 2
        },
        quota={
            'limit': 1000,
            'period': 'MONTH'
        }
    )

    usage_plan_id = usage_plan_response['id']
    print(f"Usage plan created: {usage_plan_id}")

    # Associate API key with usage plan
    client.create_usage_plan_key(
        usagePlanId=usage_plan_id,
        keyId=api_key_id,
        keyType='API_KEY'
    )
    print("API key associated with usage plan.")

def create_api(api_name, lambda_arn, user_pool_arn, user_pool_client_id):
    api_id = create_api_gateway(api_name)
    integration_id = create_lambda_integration(api_id, lambda_arn)
    authorizer_id = create_cognito_authorizer(api_id, user_pool_arn, user_pool_client_id)
    create_routes(api_id, integration_id, authorizer_id)
    create_api_key_and_usage_plan(api_id)
    return api_id

if __name__ == "__main__":
    lambda_arn = "<lambda_function_arn>"
    user_pool_arn = "arn:aws:cognito-idp:<region>:<account_id>:userpool/<user_pool_id>"
    user_pool_client_id = "<app_client_id>"

    api_id = create_api("VPC-API", lambda_arn, user_pool_arn, user_pool_client_id)
    print(f"API setup complete. API ID: {api_id}")
