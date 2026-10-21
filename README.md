# 14_DevOps_Python_Automation

backup-volume.py -
Contains two function that are also referenced in restore-volume.py:
fetch_prod_instances_to_list - returns a list of all ec2 instances having tag 'environment' = 'prod'.

search_attached_volumes - searches for all volumes attached to ec2 instances having prod tag. Returns a dictionary having ec2 instance id defined as a dictionary key and list of volume ids defined as dictionary value.

Program then selects one prod instance id and creates a snapshot for volumes attached to this instance. Program is scheduled to run every 20 seconds.
cleanup-snapshots.py - program searches for all self created volume snapshots and sorts them from the newest to oldest. It keeps only last two snapshots, the older remaining snapshots are deleted.

restore-volume.py

program retrieves all snapshot derived from a volume attached to ec2 instance having prod tag.
new volume is created based on the latest snapshot
new volume is attached to one selected ec2 instance.
