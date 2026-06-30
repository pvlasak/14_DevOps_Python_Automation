import boto3

ec2_client = boto3.client('ec2', region_name='eu-central-1')
ec2_resource = boto3.resource('ec2', region_name='eu-central-1')

instances_description = ec2_client.describe_instances()
print(instances_description)

for reservation in instances_description['Reservations']:
    for instance in reservation['Instances']:
        print(f"Status of instance {instance["InstanceId"]} is {instance['State']['Name']}")

statuses = ec2_client.describe_instance_status()
for status in statuses['InstanceStatuses']:
    instance_status = status['InstanceStatus']['Status']
    system_status = status['SystemStatus']['Status']
    print(f"Instance {status['InstanceId']} status is {instance_status} and system status is {system_status}")