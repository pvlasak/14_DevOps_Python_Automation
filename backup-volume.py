import boto3
import schedule

ec2_client = boto3.client('ec2', region_name='eu-central-1')

prod_instances = []
prod_instances_and_volumes ={}

instance_reservations = ec2_client.describe_instances(Filters=[{'Name': 'tag:environment', 'Values': ['prod']}])['Reservations']

for reservation in instance_reservations:
    for instance in (reservation['Instances']):
        prod_instances.append(instance['InstanceId'])

print(prod_instances)

for instance in prod_instances:
    volumes = ec2_client.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance]}])['Volumes']
    volume_list = []
    for volume in volumes:
        print(f"Instance {instance} has attached volume {volume['VolumeId']}")
        volume_list.append(volume['VolumeId'])
    prod_instances_and_volumes[instance] = volume_list
print(prod_instances_and_volumes)

def create_volume_snapshots(instance_id):
    attached_volumes = prod_instances_and_volumes[instance_id]
    for volume_id in attached_volumes:
        new_snapshot = ec2_client.create_snapshot(VolumeId = volume_id)
        print(new_snapshot)

schedule.every(20).seconds.do(create_volume_snapshots, prod_instances[0])

while True:
    schedule.run_pending()

