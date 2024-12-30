# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_baseline.pipeline_stack import PipelineStack

config = {
    "devAccount": {
        "awsAccountId": 390403866377,
        "awsRegion": "us-east-1"
    },
    "dev": {
        "jobs": {
            "ProcessLegislators": {
                "inputLocation": "s3://path_to_data/"
            }
        },
        "awsAccountId": 390403866377
    },
    "prod": {
        "jobs": {
            "ProcessLegislators": {
                "inputLocation": "s3://path_to_data/"
            }
        }
    }
}
def test_pipeline_created():
    app = core.App()
    stack = PipelineStack(
        app, 
        "TestPipelineStack",
        config=config,
        env=core.Environment(region='us-east-1')
    )
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::CodePipeline::Pipeline", 1)
