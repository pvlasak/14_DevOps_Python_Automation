import boto3

ec2_client = boto3.client('ec2', region_name='eu-central-1')
ec2_resource = boto3.resource('ec2', region_name='eu-central-1')

instances_description = ec2_client.describe_instances()
print(instances_description)

for reservation in instances_description['Reservations']:
    for instance in reservation['Instances']:
        print(f"Status of instance {instance["InstanceId"]} is {instance['State']['Name']}")