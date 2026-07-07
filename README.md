# 14_DevOps_Python_Automation

**branch ec2-status-check**
- `ec2-status-check.py` - uses ec2_client to check the ec2 state and instance and system status. program runs every 30 seconds.

**branch ec2-env-tags**
- `ec2-env-tags.py` - create new tags of ec2 instances running in different regions.

**branch eks_info** 
- `eks-info.py` - fetches the info about EKS cluster 

**branch volumes**
- `backup-volume.py` -
- Contains two function that are also referenced in `restore-volume.py`:
1. *fetch_prod_instances_to_list* - returns a list of all ec2 instances having tag 'environment' = 'prod'.

2. *search_attached_volumes* - searches for all volumes attached to ec2 instances having prod tag. Returns a dictionary having ec2 instance id defined as a dictionary key and list of volume ids defined as dictionary value. 

- Program then selects one prod instance id and creates a snapshot for volumes attached to this instance. Program is scheduled to run every 20 seconds. 

`cleanup-snapshots.py` - program searches for all self created volume snapshots and sorts them from the newest to oldest. It keeps only last two snapshots, the older remaining snapshots are deleted. 

`restore-volume.py` 
- program retrieves all snapshot derived from a volume attached to ec2 instance having prod tag. 
- new volume is created based on the latest snapshot
- new volume is attached to one selected ec2 instance. 

**branch website_monitoring**
- program checks if the response status on HTTP request is 200, if not it initiates a restart of nginx application container. 
- in case the request gets an error response, programs reboots the server and restarts the container 
- program uses Linode client to access the remote virtual machine on Linode platform. For this purpose the library `linode_api4` is imported. 
- To execute linux commands on virtual server the SSH client is defined by using `paramiko` library
- User is notified by an email that is being sent through `smtplib` library
- environmental variables as EMAIL_ADDRESS, EMAIL_PASSWORD and LINODE_TOKEN can be defined in Linux by *export* command:
  example: *export EMAIL_ADDRESS = value*
- 

