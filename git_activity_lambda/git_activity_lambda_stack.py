from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
)
from constructs import Construct

class GitActivityLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_.Function(
            self,
            "GitActivityLambda",
            runtime=lambda_.Runtime.PYTHON_3_13,
            handler="app.lambda_handler",
            code=lambda_.Code.from_asset("lambda_asset"),
        )
