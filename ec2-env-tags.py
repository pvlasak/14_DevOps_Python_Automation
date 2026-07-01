import boto3

ec2_client_frankfurt = boto3.client('ec2', region_name='eu-central-1')
ec2_resource_frankfurt = boto3.resource('ec2', region_name='eu-central-1')

ec2_client_paris = boto3.client('ec2', region_name='eu-west-3')
ec2_resource_paris = boto3.resource('ec2', region_name='eu-west-3')


reservations_frankfurt = ec2_client_frankfurt.describe_instances()['Reservations']
instance_ids_frankfurt = []

reservations_paris = ec2_client_paris.describe_instances()['Reservations']
instance_ids_paris= []


for reservation in reservations_frankfurt:
    for instance in reservation['Instances']:
        instance_id = (instance['InstanceId'])
        instance_ids_frankfurt.append(instance_id)


response = ec2_client_frankfurt.create_tags(
    Resources=
       instance_ids_frankfurt,
    Tags=[
        {
            'Key': 'City',
            'Value': 'Frankfurt'
        },
    ]
)

for reservation in reservations_paris:
    for instance in reservation['Instances']:
        instance_id = (instance['InstanceId'])
        instance_ids_paris.append(instance_id)


response = ec2_client_paris.create_tags(
    Resources=
       instance_ids_paris,
    Tags=[
        {
            'Key': 'City',
            'Value': 'Paris'
        },
    ]
)