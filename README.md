# 14_DevOps_Python_Automation

**branch ec2-status-check**
- `ec2-status-check.py` - uses ec2_client to check the ec2 state and instance and system status. program runs every 30 seconds.

**branch ec2-env-tags**
- `ec2-env-tags.py` - create new tags of ec2 instances running in different regions.

**branch eks_info** 
- `eks-info.py` - fetches the info about EKS cluster 

**branch volumes**
`backup-volume.py` - program searches for the ec2 instances having tag *environment:prod* and creates a dictionary of all prod instances defined as a dictionary key and list of volumes attached to instance is defined 
as a dictionary value. Program then selects one prod instance id and creates a snapshot for volumes attached to this instance. Program is scheduled to run every 20 seconds. 

`cleanup-snapshots.py` - program searches for all self created volume snapshots and sorts them from the newest to oldest. It keeps only last two snapshots, the older remaining snapshots are deleted. 

