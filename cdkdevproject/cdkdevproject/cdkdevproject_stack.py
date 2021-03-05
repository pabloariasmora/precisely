import os

from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    core
)

if not os.environ.get('preciselyAPIKey'):
    raise Exception('Missing preciselyAPIKey env variable')

if not os.environ.get('preciselyAPISECRET'):
    raise Exception('Missing preciselyAPISECRET env variable')


class CdkdevprojectStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines an AWS Lambda resource
        precisely_lambda = _lambda.Function(
            self, 'PreciselyHandler',
            # TODO
            # There is a DeprecationWarning Associated to this version
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='precisely.handler',
            environment={
                'preciselyAPIKey': os.environ['preciselyAPIKey'],
                'preciselyAPISECRET': os.environ['preciselyAPISECRET'],
                'URL': 'api.precisely.com',
                'MinLengthAllowed': '3'
            }
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=precisely_lambda,
        )