# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from typing import Dict
from os import path
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_s3_deployment as s3deploy,
    RemovalPolicy,
    CfnTag,
)
from constructs import Construct

class LambdaAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, config:Dict, stage:str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ##########################################################################
        ##                                                                      ##
        ##                INSERTAR ARCHIVOS .PY EN S3 BUCKETS                   ##
        ##                                                                      ##
        ##                                                                      ##
        ##########################################################################

        self.lambda_bucket = s3.Bucket.from_bucket_arn(self, "lambda-Bucket",
            bucket_arn  = f"arn:aws:s3:::s3-scripts-bucket-{str(config[stage]['awsAccountId'])}"
        )

        self.bucket_deployment = s3deploy.BucketDeployment(self, "Populate-lambda-Bucket",
            sources=[s3deploy.Source.asset(
                path.join(path.dirname(__file__), "project_files/lambda"))],
            destination_bucket=self.lambda_bucket,
            prune = False, 
        )
         
        ##########################################################################
        ##                                                                      ##
        ##                 CREACION DE AWS CDK LAMBDA FUNCTIONS                 ##
        ##                                                                      ##
        ##                                                                      ##
        ##########################################################################

        self.lam_data_extraction = lambda_.CfnFunction(self, "lam_data_extraction",
            code=lambda_.CfnFunction.CodeProperty(
                s3_bucket=f"s3-scripts-bucket-{str(config[stage]['awsAccountId'])}",
                s3_key="lambda/lam_data_extraction.zip",
            ),
            ## este rol de servicio se podría definir con IaC pero acá se creó desde la consola y se pone el arn
            role=f"arn:aws:iam::{str(config[stage]['awsAccountId'])}:role/service-role/first-test-role-vn00mm7y", 
            # the properties below are optional
            architectures=["x86_64"], ###
            description="",
            ephemeral_storage=lambda_.CfnFunction.EphemeralStorageProperty(
                size=1024
            ),
            function_name=f"lam_data_extraction",
            layers=[f"arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python312:15"],
            handler="lambda_function.lambda_handler",
            memory_size=1024,
            runtime="python3.12",
            tags=[CfnTag(
                key="Name",
                value=f"lam_data_extraction"
            )],
            timeout=300
        ) 
        self.lam_data_extraction.apply_removal_policy(RemovalPolicy.RETAIN)
        self.lam_data_extraction.node.add_dependency(self.bucket_deployment)

        self.lam_insert_data_catalog = lambda_.CfnFunction(self, "lam_insert_data_catalog",
            code=lambda_.CfnFunction.CodeProperty(
                s3_bucket=f"s3-scripts-bucket-{str(config[stage]['awsAccountId'])}",
                s3_key="lambda/lam_insert_data_catalog.zip",
            ),
            role=f"arn:aws:iam::{str(config[stage]['awsAccountId'])}:role/service-role/first-test-role-vn00mm7y",
            # the properties below are optional
            architectures=["x86_64"], ###
            description="",
            ephemeral_storage=lambda_.CfnFunction.EphemeralStorageProperty(
                size=1024
            ),
            function_name=f"lam_insert_data_catalog",
            layers=[f"arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python312:15"],
            handler="lambda_function.lambda_handler",
            memory_size=1024,
            runtime="python3.12",
            tags=[CfnTag(
                key="Name",
                value=f"lam_insert_data_catalog"
            )],
            timeout=300
        ) 
        self.lam_insert_data_catalog.apply_removal_policy(RemovalPolicy.RETAIN)
        self.lam_insert_data_catalog.node.add_dependency(self.bucket_deployment)

        self.lam_transformar_precipitaciones = lambda_.CfnFunction(self, "lam_transformar_precipitaciones",
            code=lambda_.CfnFunction.CodeProperty(
                s3_bucket=f"s3-scripts-bucket-{str(config[stage]['awsAccountId'])}",
                s3_key="lambda/lam_transformar_precipitaciones.zip",
            ),
            role=f"arn:aws:iam::{str(config[stage]['awsAccountId'])}:role/service-role/first-test-role-vn00mm7y",
            # the properties below are optional
            architectures=["x86_64"], ###
            description="",
            ephemeral_storage=lambda_.CfnFunction.EphemeralStorageProperty(
                size=1024
            ),
            function_name=f"lam_transformar_precipitaciones",
            layers=[f"arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python312:15"],
            handler="lambda_function.lambda_handler",
            memory_size=1024,
            runtime="python3.12",
            tags=[CfnTag(
                key="Name",
                value=f"lam_transformar_precipitaciones"
            )],
            timeout=300
        ) 
        self.lam_transformar_precipitaciones.apply_removal_policy(RemovalPolicy.RETAIN)
        self.lam_transformar_precipitaciones.node.add_dependency(self.bucket_deployment)