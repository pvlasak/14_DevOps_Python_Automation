import boto3
from operator import itemgetter

ec2_client = boto3.client('ec2', region_name='eu-central-1')

snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])
print(snapshots['Snapshots'])

for snapshot in snapshots['Snapshots']:
    print(snapshot['StartTime'])

sorted_by_date = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

# deleting all my snapshots expect of last two newest
for snapshot in sorted_by_date[2:]:
    response = ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])

    print(response)