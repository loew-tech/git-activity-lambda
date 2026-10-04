from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


class GitActivityLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        github_token = secretsmanager.Secret.from_secret_name_v2(
            self,
            "GitHubToken",
            "git-activity/github-token",
        )

        activity_lambda = lambda_.Function(
            self,
            "GitActivityLambda_0_1",
            runtime=lambda_.Runtime.PYTHON_3_13,
            handler="app.lambda_handler",
            code=lambda_.Code.from_asset("lambda_asset"),
            environment={
                "GITHUB_TOKEN_SECRET": github_token.secret_name,
                "GITHUB_USERNAME": "loew-tech"
            },
        )

        github_token.grant_read(activity_lambda)