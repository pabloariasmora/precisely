#!/usr/bin/env python3

from aws_cdk import core

from cdkdevproject.cdkdevproject_stack import CdkdevprojectStack


app = core.App()
CdkdevprojectStack(app, "cdkdevproject", env={'region': 'us-west-2'})

app.synth()
