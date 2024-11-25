from cdktf import TerraformStack
from constructs import Construct
from imports.aws.security_group import SecurityGroup
from imports.aws.vpc_security_group_egress_rule import VpcSecurityGroupEgressRule
from imports.aws.vpc_security_group_ingress_rule import VpcSecurityGroupIngressRule
from imports.aws.instance import Instance
from variables import NetworkConfig
from providers import create_aws_provider

class InstanceStack(TerraformStack):
    def __init__(self, scope: Construct, id: str, config: NetworkConfig, network_stack):
        super().__init__(scope, id)
        
        # Create AWS Provider
        create_aws_provider(self, id)

        # Default security group for instance
        webSecurityGroup = SecurityGroup(self, "WebSG",
            description="Allow inbound traffic and all outbound traffic",
            name="securityGroup",
            tags={
                "Name": "Allow inbound traffic and all outbound traffic"
            },
            vpc_id=network_stack.vpc_id,
        )

        # Allow All
        VpcSecurityGroupEgressRule(self, "allow_all_traffic_inbound_ipv4",
            cidr_ipv4="0.0.0.0/0",
            ip_protocol="-1",
            security_group_id=webSecurityGroup.id
        )

         #Allow HHTPS
        VpcSecurityGroupIngressRule(self, "allow_https_ipv4",
            cidr_ipv4="0.0.0.0/0",
            from_port=443,
            ip_protocol="tcp",
            security_group_id=webSecurityGroup.id,
            to_port=443
        )

        # Allow SSH
        VpcSecurityGroupIngressRule(self, "allow_ssh_ipv4",
            cidr_ipv4="0.0.0.0/0",
            from_port=22,
            ip_protocol="tcp",
            security_group_id=webSecurityGroup.id,
            to_port=22
        )

        # EC2 Instance
        Instance(self, "WebServer",
            ami="ami-00385a401487aefa4",
            instance_type="t2.micro",
            subnet_id=network_stack.public_subnet_id,
            vpc_security_group_ids=[webSecurityGroup.id],
            tags={
                "Name": f"{config.projectName}-web-server",
                "Environment": config.environment
            }
        )