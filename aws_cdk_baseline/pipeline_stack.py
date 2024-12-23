# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from typing import Dict
from aws_cdk import (
    Environment,
    Stack,
    aws_codecommit as codecommit,
    aws_iam as iam
)
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, CodeBuildStep, ManualApprovalStep, ShellStep
from helper import create_archive
from aws_cdk_baseline.app_stage import GlueAppStage


class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config: Dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        archive_file = create_archive()

        source = CodePipelineSource.connection("jzam0ra/pruebaTecnicaNQ", "main",
            connection_arn="arn:aws:codeconnections:us-east-1:390403866377:connection/3df4df9e-0eb1-4ffa-9979-8f61dbd46ade"
        )
        
        pipeline = CodePipeline(self, "DataPipeline",
            pipeline_name="DataPipeline",
            cross_account_keys=True,
            docker_enabled_for_synth=True,
            synth=CodeBuildStep("CdkSynth_UnitTest",
                input=source,
                install_commands=[
                    "pip install -r requirements-dev.txt",
                    "pip install -r requirements.txt",
                    "npm install -g aws-cdk",
                ],
                commands=[
                    "cdk synth -c stage=dev",
                    # Unit test for CDK stack
                    "python -m pytest",
                ],
            )
        )
        
        # Dev deployment
        dev_stage_name = "DeployDev"
        if config["devAccount"]["awsAccountId"] == config["devAccount"]["awsAccountId"] and config["devAccount"]["awsRegion"] == config["devAccount"]["awsRegion"]:
            dev_env = None
        else:
            dev_env = Environment(
                account=str(config["devAccount"]["awsAccountId"]), 
                region=config["devAccount"]["awsRegion"]
            )
        dev_stage_app = GlueAppStage(
            self, 
            dev_stage_name,
            config=config,
            stage="dev",
            env=dev_env
        )
        dev_stage = pipeline.add_stage(dev_stage_app)
        dev_stage.add_pre(ManualApprovalStep("Approval"))