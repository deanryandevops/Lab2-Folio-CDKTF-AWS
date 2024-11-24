from cdktf import TerraformStack
from constructs import Construct
from imports.aws import Instance, SecurityGroup
from variables import NetworkConfig

class InstanceStack(TerraformStack):
    def __init__(self, scope: Construct, id: str, config: NetworkConfig, NetworkStack):
        super().__init__(scope, id)
        
        #security group
        securityGroup = SecurityGroup(self, "security-group",
            name=f"{config.project_name}-security-group",
            vpc_id=NetworkStack.vpc_id,         
            ingress=[{
                "protocol": "tcp",
                "from_port": 443,
                "to_port": 443,
                "cidr_blocks": ["0.0.0.0/0"],
                "description": "HTTPS"
            }, 
            {
                "protocol": "tcp",
                "from_port": 22,
                "to_port": 22,
                "cidr_blocks": ["10.0.1.0/24"],
                "description": "SSH"
            }],       
            egress=[{
                "protocol": "-1",
                "from_port": 0,
                "to_port": 0,
                "cidr_blocks": ["0.0.0.0/0"],
                "description": "All outbound traffic"
            }],
            
            tags={
                "Name": f"{config.project_name}-security-group",
                "Environment": config.environment
            }
        )

        # EC2 Instance
        Instance(self, "Public-Instance",
            ami="ami-00385a401487aefa4",
            instance_type="t2.micro",
            subnet_id=NetworkStack.publicSubnetCidr,
            vpc_security_group_ids=[securityGroup.id],
            tags={
                "Name": f"{config.project_name}-web-server",
                "Environment": config.environment
            }
        )



             # Security Group for public instances
    Properties:
      GroupName: "public-security-group"
      GroupDescription: "Allow traffic inbound for ssh on public subnet and https and allow all outbound"
      VpcId: !Ref FridayHITTVPC
      SecurityGroupIngress: # this is inbounds configuration
        - IpProtocol: tcp # SSH 
          FromPort: 22
          ToPort: 22
          CidrIp: 10.0.1.0/24
        - IpProtocol: tcp # HTTPS
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
      Tags:
        - Key: Name
          Value: public-security-group

