import json
import pytest

from aws_cdk import core
from cdkdevproject.cdkdevproject_stack import CdkdevprojectStack


def get_template():
    app = core.App()
    CdkdevprojectStack(app, "cdkdevproject")
    return json.dumps(app.synth().get_stack("cdkdevproject").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
