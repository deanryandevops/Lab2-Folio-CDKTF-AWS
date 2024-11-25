from cdktf import TerraformStack
from constructs import Construct
from imports.aws import Instance, SecurityGroup
from variables import NetworkConfig

class InstanceStack(TerraformStack):
    def __init__(self, scope: Construct, id: str, config: NetworkConfig, NetworkStack):
        super().__init__(scope, id)
        
        # Security Group
        web_sg = SecurityGroup(self, "public-security-group",
            name=f"{config.project_name}-public-security-group",
            vpc_id=network_stack.vpc_id,



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

