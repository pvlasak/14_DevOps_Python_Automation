import boto3
import schedule

ec2_client = boto3.client('ec2', region_name='eu-central-1')


def fetch_prod_instances_to_list():
    prod_instances = []
    instance_reservations = ec2_client.describe_instances(Filters=[{'Name': 'tag:environment', 'Values': ['prod']}])['Reservations']

    for reservation in instance_reservations:
        for instance_item in (reservation['Instances']):
            prod_instances.append(instance_item['InstanceId'])
    return prod_instances


def search_attached_volumes(list_of_instances: list):
    prod_instances_and_volumes = {}
    for instance_item in list_of_instances:
        volumes = ec2_client.describe_volumes(Filters=[{'Name': 'attachment.instance-id', 'Values': [instance_item]}])['Volumes']
        volume_list = []
        for volume in volumes:
            print(f"Instance {instance_item} has attached volume {volume['VolumeId']}")
            volume_list.append(volume['VolumeId'])
        prod_instances_and_volumes[instance_item] = volume_list
    return prod_instances_and_volumes


def create_volume_snapshots(instances_and_volumes: dict):
    # grabs only the first instance for simplicity
    first_instance = list(instances_and_volumes.keys())[0]
    attached_volumes = instances_and_volumes[first_instance]
    for volume_id in attached_volumes:
        new_snapshot = ec2_client.create_snapshot(VolumeId = volume_id)
        print(new_snapshot)

def main():
    prod_ec2_instances_as_list = fetch_prod_instances_to_list()
    ec2_volumes_dict = search_attached_volumes(prod_ec2_instances_as_list)
    schedule.every(20).seconds.do(create_volume_snapshots, ec2_volumes_dict)

    while True:
        schedule.run_pending()

if __name__ == "__main__":
    main()


