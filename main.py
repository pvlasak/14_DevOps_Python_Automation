import boto3

client = boto3.client('ec2')

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
