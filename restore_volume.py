import boto3
from backup_volume import fetch_prod_instances_to_list
from backup_volume import search_attached_volumes
from operator import itemgetter


ec2_client = boto3.client('ec2', region_name='eu-central-1')
ec2_resource = boto3.resource('ec2', region_name='eu-central-1')

production_instances = fetch_prod_instances_to_list()
production_instances_and_volumes = search_attached_volumes(production_instances)
print(production_instances_and_volumes)

instance_name = list(production_instances_and_volumes.keys())[0]
snapshot_description = ec2_client.describe_snapshots(
    Filters=[
        {
            'Name': 'volume-id',
            'Values': production_instances_and_volumes[instance_name]
        },
    ])
volume_snapshots = snapshot_description['Snapshots']
if len(volume_snapshots) == 0:
    print("No snapshots attached to volume are available.")
else:
    sorted_snapshots = sorted(volume_snapshots, key=itemgetter('StartTime'), reverse=True)
    latest_snapshot = sorted_snapshots[0]
    print("Newest snapshot identified.")
# keeping latest snapshot and deleting remaining ones
    if len(sorted_snapshots) > 1:
        for snapshot in sorted_snapshots[1:]:
            response = ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            print(f"Snapshot {snapshot['SnapshotId']} deleted")

    volume_from_snapshot = ec2_client.create_volume(SnapshotId=latest_snapshot['SnapshotId'], AvailabilityZone='eu-central-1b')
    volume_id = volume_from_snapshot['VolumeId']
    print(f"Volume of id {volume_from_snapshot['VolumeId']} is created from snapshot {latest_snapshot['SnapshotId']}.")

    while True:
        volume_state = ec2_resource.Volume(volume_id).state
        print(volume_state)
        if volume_state == 'available':
            print(f"Restored volume is attached to instance {instance_name}.")
            ec2_resource.Instance(instance_name).attach_volume(
                VolumeId=volume_id,
                Device='/dev/xvdc'
            )
            break



