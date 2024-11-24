#!/usr/bin/env python
import os
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from imports.aws.provider import AwsProvider
from imports.aws.instance import Instance

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        region = os.getenv("AWS_DEFAULT_REGION")

        # Initialize the AWS provider
        AwsProvider(self, "AWS", region=region)

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
