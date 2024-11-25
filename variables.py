from dataclasses import dataclass

@dataclass
class NetworkConfig:
    vpcCidr: str = "10.0.0.0/16"
    publicSubnetCidr: str = "10.0.1.0/24"
    privateSubnetCidr: str = "10.0.2.0/24"
    availability_zone: str = "eu-west-1"
    environment: str = "dev"
    projectName: str = "Lab2-folio-CDKTF-AWS"