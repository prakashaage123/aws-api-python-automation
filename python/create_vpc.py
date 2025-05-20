import boto3

def create_vpc():
    ec2 = boto3.client('ec2')
    response = ec2.create_vpc(
        CidrBlock='10.0.0.0/16',
        AmazonProvidedIpv6CidrBlock=False
    )
    vpc_id = response['Vpc']['VpcId']
    
    ec2.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': 'api-vpc'}])
    
    return vpc_id

def create_subnets(vpc_id):
    ec2 = boto3.client('ec2')

    subnet_a = ec2.create_subnet(
        CidrBlock='10.0.1.0/24',
        VpcId=vpc_id,
        AvailabilityZone='us-east-1a'
    )

    subnet_b = ec2.create_subnet(
        CidrBlock='10.0.2.0/24',
        VpcId=vpc_id,
        AvailabilityZone='us-east-1b'
    )

    return [subnet_a['Subnet']['SubnetId'], subnet_b['Subnet']['SubnetId']]

def create_vpc_and_subnets():
    vpc_id = create_vpc()
    subnet_ids = create_subnets(vpc_id)
    return vpc_id, subnet_ids

if __name__ == "__main__":
    vpc_id, subnet_ids = create_vpc_and_subnets()
    print(f"Created VPC with ID {vpc_id} and Subnets {subnet_ids}")
