#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from imports.aws.provider import AwsProvider
from imports.aws.instance import Instance

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # Initialize the AWS provider
        AwsProvider(self, "AWS", 
        #access_key = "my-access-key",
        #secret_key = "my-secret-key",
        region="eu-west-1")

        # Define an EC2 instance
        instance = Instance(self, "compute",
                            ami="ami-0fcc0bef51bad3cb2",
                            instance_type="t2.micro",
                            tags={"Name": "CDKTF-Demo"},
                            )


        # Output the public IP of the instance
        TerraformOutput(self, "public_ip",
                        value=instance.public_ip,
                        description="The public IP of the EC2 instance"
                        )

# Create the app and stack
app = App()
stack = MyStack(app, "aws_instance")

# Synthesize the Terraform configuration
app.synth()
