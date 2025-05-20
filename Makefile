.PHONY: create_vpc create_s3_bucket create_lambda create_api_gateway

create_vpc:
	python python/create_vpc.py

create_s3_bucket:
	python python/create_s3_bucket.py

create_lambda:
	python python/create_lambda.py

create_api_gateway:
	python python/create_api_gateway.py
