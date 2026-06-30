import boto3

client = boto3.client('ec2', region_name='us-east-1')
resource = boto3.resource('ec2', region_name='eu-west-3')

vpc_paris = resource.create_vpc(
    CidrBlock='10.0.0.0/16'
)
vpc_paris.create_subnet(
    CidrBlock='10.0.10.0/24',
)
vpc_paris.create_subnet(
    CidrBlock='10.0.20.0/24',
)
vpc_paris.create_tags(
    Tags=[
        {'Key': 'Name',
        'Value': 'Paris-VPC'
         },
    ]
)

all_available_vpcs = client.describe_vpcs()
all_vpcs = all_available_vpcs['Vpcs']

print(type(all_available_vpcs))
print(type(all_vpcs))

for vpc in all_vpcs:
    vpc_id = vpc["VpcId"]
    cidr_block_association_sets = vpc["CidrBlockAssociationSet"]
    print(f"CidrBlockAssociationSet is type of {type(cidr_block_association_sets)}")

    for set_item in cidr_block_association_sets:
        print(f"CidrBlockAssociationSet Item is type of {type(set_item)}")
        cidr_block = set_item["CidrBlock"]
    print(f"In your region the VPC having ID {vpc_id} and CIDR block {cidr_block} is available.")
