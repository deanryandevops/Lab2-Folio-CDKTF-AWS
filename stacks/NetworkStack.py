from cdktf import TerraformStack
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from imports.aws import AwsProvider, Vpc, Subnet, InternetGateway, InternetGatewayAttachment, RouteTable, RouteTableAssociation
from variables import NetworkConfig

class NetworkStack(TerraformStack):
    def __init__(self, scope: Construct, id: str, config: NetworkConfig):
        super().__init__(scope, id)

        # AWS provider, regions coming from variables.py
        AwsProvider(self, "AWS",
            region= config.availability_zone     
        )

        # VPC
        vpc = Vpc(self, f"{config.project_name}-VPC",
            cidr_block=config.vpc_cidr,
            tags={
                "Name": f"{config.project_name}-VPC",
                "Environment": config.environment
            }
        )

        # Internet Gateway
        internetGateway = InternetGateway(self, "InternetGateway",
            vpc_id=vpc.id,
            tags={
                "Name": f"{config.project_name}-InternetGateway",
                "Environment": config.environment
            }
        )

        # Attach the Internet Gateway to the VPC
        internetGatewayAttachment = InternetGatewayAttachment(self, "InternetGatewayAttachment",
                                  vpc_id=vpc.id,
                                  internet_gateway_id=internetGateway.id,
                                  tags={
                                        "Name": f"{config.project_name}-InternetGateway",
                                        "Environment": config.environment
                                  }
        )

        # Public Subnet
        publicSubnet = Subnet(self, "PublicSubnet",
            vpc_id=vpc.id,
            cidr_block=config.public_subnet_cidr,
            availability_zone=config.availability_zone,
            map_public_ip_on_launch=True,
            tags={
                "Name": f"{config.project_name}-public-subnet",
                "Environment": config.environment
            }
        )

         # Private Subnet
        private_subnet = Subnet(self, "PrivateSubnet",
            vpc_id=vpc.id,
            cidr_block=config.private_subnet_cidr,
            availability_zone=config.availability_zone,
            tags={
                "Name": f"{config.project_name}-private-subnet",
                "Environment": config.environment
            }
        )

        # Public Route Table
        publicRouteTable = RouteTable(self, "PublicRouteTable",
            vpc_id=vpc.id,
            route=[{
                "cidr_block": "0.0.0.0/0",
                "gateway_id": internetGateway.id
            }],
            tags={
                "Name": f"{config.project_name}-public-route-table",
                "Environment": config.environment
            }
        )

         # Route Table Association
        RouteTableAssociation(self, "PublicRouteTableAssociation",
            subnet_id=publicSubnet.id,
            route_table_id=publicRouteTable.id
        )