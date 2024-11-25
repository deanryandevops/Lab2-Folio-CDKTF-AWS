from cdktf import TerraformStack
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from imports.aws.provider import AwsProvider
from imports.aws.vpc import Vpc
from imports.aws.subnet import Subnet
from imports.aws.internet_gateway import InternetGateway
from imports.aws.internet_gateway_attachment import InternetGatewayAttachment
from imports.aws.route_table import RouteTable
from imports.aws.route_table_association import RouteTableAssociation
from variables import NetworkConfig
import os
from providers import create_aws_provider
from imports.aws.route import Route

class NetworkStack(TerraformStack):
    def __init__(self, scope: Construct, id: str, config: NetworkConfig):
        super().__init__(scope, id)

        # Create AWS Provider
        create_aws_provider(self, id)

        # VPC
        vpc = Vpc(self, f"{config.projectName}-VPC",
            cidr_block=config.vpcCidr,
            tags={
                "Name": f"{config.projectName}-VPC",
                "Environment": config.environment
            }
        )

        # Internet Gateway
        internetGateway = InternetGateway(self, "InternetGateway", vpc_id=vpc.id,
            tags={
                "Name": f"{config.projectName}-InternetGateway",
                "Environment": config.environment
            }
        )

        # Public Subnet
        publicSubnet = Subnet(self, "PublicSubnet",
            vpc_id=vpc.id,
            cidr_block=config.publicSubnetCidr,
            availability_zone="eu-west-1a",
            map_public_ip_on_launch=True,
            tags={
                "Name": f"{config.projectName}-public-subnet",
                "Environment": config.environment
            }
        )

        # Private Subnet
        privateSubnet = Subnet(self, "PrivateSubnet",
            vpc_id=vpc.id,
            cidr_block=config.privateSubnetCidr,
            availability_zone="eu-west-1a",
            tags={
                "Name": f"{config.projectName}-private-subnet",
                "Environment": config.environment
            }
        )

        # Create a Route Table
        route_table = RouteTable(self, "MyRouteTable", vpc_id=vpc.id)

        # Create a default route to the internet gateway
        Route(self, "DefaultRoute",
              route_table_id=route_table.id,
              destination_cidr_block="0.0.0.0/0",
              gateway_id=internetGateway.id)

        # Associate the route table with the subnet
        RouteTableAssociation(self, "RouteTableAssociation",
                              route_table_id=route_table.id,
                              subnet_id=publicSubnet.id)

        self.vpc_id = vpc.id
        self.public_subnet_id = publicSubnet.id
        self.private_subnet_id = privateSubnet.id