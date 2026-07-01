import boto3
import schedule

ec2_client = boto3.client('ec2', region_name='eu-central-1')
ec2_resource = boto3.resource('ec2', region_name='eu-central-1')


def check_instance_status():
    statuses = ec2_client.describe_instance_status()
    for status in statuses['InstanceStatuses']:
        state = status['InstanceState']['Name']
        instance_status = status['InstanceStatus']['Status']
        system_status = status['SystemStatus']['Status']
        print(f"Instance {status['InstanceId']} has state {state} and instance status is {instance_status} and system status is {system_status}")
    print("*************************************** \n")
schedule.every(30).seconds.do(check_instance_status)

while True:
    schedule.run_pending()