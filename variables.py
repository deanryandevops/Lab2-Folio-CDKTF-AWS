from dataclasses import dataclass

@dataclass
class NetworkConfig:
    vpc_cidr: str = "10.0.0.0/16"
    public_subnet_cidr: str = "10.0.1.0/24"
    private_subnet_cidr: str = "10.0.2.0/24"
    availability_zone: str = "eu-west-1"
    environment: str = "dev"
    project_name: str = "Lab2-folio-CDKTF-AWS"