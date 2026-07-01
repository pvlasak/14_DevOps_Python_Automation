provider "aws" {
    region = "eu-central-1"
}

variable vpc_cidr_block {}
variable private_subnets {}
variable public_subnets {}
variable instance_types {}

data "aws_availability_zones" "azs" {}


module "myapp-vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 6.0"

  name = "myapp-vpc"
  cidr = var.vpc_cidr_block

  azs = data.aws_availability_zones.azs.names
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets

  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_hostnames = true

  tags = {
	"kubernetes.io/cluster/myapp-eks-cluster" = "shared"
  }
  public_subnet_tags = {
    "kubernetes.io/cluster/myapp-eks-cluster" = "shared"
    "kubernetes.io/role/elb"                    = "1"
  }
  private_subnet_tags = {
    "kubernetes.io/cluster/myapp-eks-cluster" = "shared"
    "kubernetes.io/role/internal-elb"           = "1"
  }
}

output "azs" {
    value = data.aws_availability_zones.azs.names
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0"

  name               = "myapp-eks-cluster"
  kubernetes_version = "1.33"

  addons = {
    coredns                = {}
    eks-pod-identity-agent = {
      before_compute = true
    }
    kube-proxy             = {}
    vpc-cni                = {
      before_compute = true
    }
  }

  endpoint_public_access = true
  enable_cluster_creator_admin_permissions = true

  vpc_id                   =  module.myapp-vpc.vpc_id
  subnet_ids               =  module.myapp-vpc.private_subnets

  # EKS Managed Node Group(s)
  eks_managed_node_groups = {
    example = {
      # Starting on 1.30, AL2023 is the default AMI type for EKS managed node groups
      ami_type       = "AL2023_x86_64_STANDARD"
      instance_types = var.instance_types

      min_size     = 1
      max_size     = 2
      desired_size = 2
    }
  }

  tags = {
	environment = "development"
	application = "myapp"
  }
}
