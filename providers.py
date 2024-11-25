from imports.aws.provider import AwsProvider
from constructs import Construct

# this allows the stacks to use the same provider
def create_aws_provider(scope: Construct, id: str):
    return AwsProvider(scope, f"{id}-aws-provider",
        region="eu-west-1"
    )