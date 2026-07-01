import boto3

eks_client = boto3.client('eks')

cluster_list = eks_client.list_clusters()

clusters = cluster_list['clusters']

for cluster in clusters:
    cluster_info = eks_client.describe_cluster(name= cluster)['cluster']
    version = cluster_info['version']
    endpoint = cluster_info['endpoint']
    status = cluster_info['status']

    print(f"EKS cluster named {cluster} has Kubernetes version {version}, is accessible at {endpoint} and has current status {status}.")