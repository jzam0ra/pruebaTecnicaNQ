# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from typing import Dict
import aws_cdk as cdk
from constructs import Construct
from aws_cdk_baseline.lambda_app_stack import LambdaAppStack

class GlueAppStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, config:Dict, stage:str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_app_stack = LambdaAppStack(self, "LambdaAppStack", config, stage)
