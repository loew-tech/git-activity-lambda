import unittest

from aws_cdk import App, assertions

from git_activity_lambda.git_activity_lambda_stack import GitActivityLambdaStack


class TestGitActivityLambdaStack(unittest.TestCase):

    def setUp(self):
        app = App()

        self.stack = GitActivityLambdaStack(
            app,
            "TestGitActivityLambdaStack",
        )

        self.template = assertions.Template.from_stack(self.stack)

    def test_lambda_configuration(self):
        self.template.has_resource_properties(
            "AWS::Lambda::Function",
            {
                "Runtime": "python3.13",
                "Handler": "app.lambda_handler",
                "Environment": {
                    "Variables": {
                        "GITHUB_TOKEN_SECRET": "git-activity/github-token",
                    },
                },
            },
        )

    def test_lambda_has_secrets_manager_permission(self):
        self.template.has_resource_properties(
            "AWS::IAM::Policy",
            {
                "PolicyDocument": {
                    "Statement": assertions.Match.array_with(
                        [
                            assertions.Match.object_like(
                                {
                                    "Action": assertions.Match.array_with(
                                        [
                                            "secretsmanager:GetSecretValue",
                                        ]
                                    ),
                                    "Effect": "Allow",
                                }
                            )
                        ]
                    )
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
