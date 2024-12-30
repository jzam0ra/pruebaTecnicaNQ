# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_baseline.lambda_app_stack import LambdaAppStack

config = {
    "devAccount": {
        "awsAccountId": 390403866377,
        "awsRegion": "us-east-1"
    },
    "dev": {
        "awsAccountId": 390403866377
    }
}

def remove_key(obj, key_to_remove):
    if isinstance(obj, dict):
        obj.pop(key_to_remove, None)
        for k, v in obj.items():
            remove_key(v, key_to_remove)
    elif isinstance(obj, list):
        for item in obj:
            remove_key(item, key_to_remove)


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
    templateJson = template.to_json() 
    remove_key(templateJson, "S3Key")
    remove_key(snapshot, "S3Key")
    assert templateJson == snapshot
