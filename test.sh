#!/bin/bash

# Replace with actual values after deployment
API_URL="<your_api_url>"
API_KEY="<your_api_key>"

# Create VPC
curl -X POST "$API_URL/create-vpc" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json"

# Get VPC info
curl "$API_URL/vpc-info" \
  -H "x-api-key: $API_KEY"
