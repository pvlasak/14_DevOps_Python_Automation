import boto3

ec2_client = boto3.client('ec2', region_name='eu-central-1')
ec2_resource = boto3.resource('ec2', region_name='eu-central-1')

def fetch_prod_instances():
    prod_instances_and_volumes ={}
    prod_instances = []
    instance_reservations = ec2_client.describe_instances(Filters=[{'Name': 'tag:environment', 'Values': ['prod']}])['Reservations']
    for reservation in instance_reservations:
        for instance in (reservation['Instances']):
            prod_instances.append(instance['InstanceId'])
