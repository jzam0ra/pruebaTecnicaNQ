# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_baseline.lambda_app_stack import LambdaAppStack

config = {
    "devAccount": {
        "awsAccountId": 390403866377,
        "awsRegion": "us-east-1"
    }
}

def test_glue_app_stack_snapshot(snapshot):
    app = core.App()
    stack = LambdaAppStack(
        app, 
        "TestGlueAppStack",
        config=config,    
        stage="dev",           
        env=core.Environment(region='us-east-1')
    )
    template = assertions.Template.from_stack(stack)
    assert template.to_json() == snapshot
