from aws_cdk import (
    Stack,
    Duration,
    aws_apigatewayv2_alpha as apigwv2,
    aws_lambda as _lambda,
    aws_secretsmanager as sm,
)
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration
from constructs import Construct


class ChatGptPluginLambdaBackedStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        botCredsSecret = sm.Secret.from_secret_name_v2(self, "BotCreds", "BotCreds")

        query_lambda = _lambda.Function(
            self,
            "QueryLambda",
            function_name="ChatGPTPluginQueryLambda",
            runtime=_lambda.Runtime.FROM_IMAGE,
            code=_lambda.Code.from_asset_image("lambdas/hello1"),
            handler=_lambda.Handler.FROM_IMAGE,
            timeout=Duration.seconds(30),
        )

        botCredsSecret.grant_read(query_lambda)

        hello2_lambda = _lambda.Function(
            self,
            "Hello2Handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambdas/"),
            handler="hello.main2",
        )

        api = apigwv2.HttpApi(self, "Endpoint")
        api.add_routes(
            path="/hello1",
            methods=[apigwv2.HttpMethod.GET],
            integration=HttpLambdaIntegration("Lambda1", query_lambda),
        )
        api.add_routes(
            path="/hello2",
            methods=[apigwv2.HttpMethod.GET],
            integration=HttpLambdaIntegration("Lambda2", hello2_lambda),
        )
