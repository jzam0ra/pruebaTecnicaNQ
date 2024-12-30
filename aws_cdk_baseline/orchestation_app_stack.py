from typing import Dict
from os import path
from aws_cdk import (
    Stack,
    aws_stepfunctions as stepfunctions,
    aws_scheduler as scheduler,
    RemovalPolicy,
)
from constructs import Construct
import json


class OrchestationAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, config:Dict, stage:str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)



        ##########################################################################
        ##                                                                      ##
        ##                   CREACION DE AWS STEP FUNCTIONS                     ##
        ##                                                                      ##
        ##                                                                      ##
        #########################################################################

        self.definition_stm = {
            "QueryLanguage": "JSONata",
            "Comment": "A description of my state machine",
            "StartAt": "Lambda Invoke",
            "States": {
                "Lambda Invoke": {
                    "Type": "Task",
                    "Resource": "arn:aws:states:::lambda:invoke",
                    "Output": "{% $states.result.Payload %}",
                    "Arguments": {
                        "FunctionName": "arn:aws:lambda:us-east-1:390403866377:function:first-test:$LATEST"
                    },
                    "Retry": [
                        {
                            "ErrorEquals": [
                                "Lambda.ServiceException",
                                "Lambda.AWSLambdaException",
                                "Lambda.SdkClientException",
                                "Lambda.TooManyRequestsException"
                            ],
                            "IntervalSeconds": 1,
                            "MaxAttempts": 3,
                            "BackoffRate": 2,
                            "JitterStrategy": "FULL"
                        }
                    ],
                    "End": True
                }
            }
        }


        self.stm_launch_lambda = stepfunctions.CfnStateMachine(self, "stm_launch_lambda",
            role_arn=f"arn:aws:iam::{str(config[stage]['awsAccountId'])}:role/stepfunctionsrole",
            state_machine_name=f"stm_launch_lambda",
            state_machine_type="STANDARD",
            # the properties below are optional
            definition_string=json.dumps(self.definition_stm),
            tags=[stepfunctions.CfnStateMachine.TagsEntryProperty(
                key="Name",
                value=f"stm_launch_lambda"
            )],
        )
        self.stm_launch_lambda.apply_removal_policy(RemovalPolicy.RETAIN)


        ##########################################################################
        ##                                                                      ##
        ##                   CREACION DE AWS EVENTBRIDGE RULES                  ##
        ##                             Y SCHEDULERS                             ##
        ##                                                                      ##
        ##########################################################################
        self.schedule_input = {}
        self.import_schedule = scheduler.CfnSchedule(self, "import_schedule",
            flexible_time_window=scheduler.CfnSchedule.FlexibleTimeWindowProperty(
                mode="OFF",
            ),
            schedule_expression="cron(0 9 * * ? *)",
            target=scheduler.CfnSchedule.TargetProperty(
                arn=f"arn:aws:states:us-east-1:{str(config[stage]['awsAccountId'])}:stateMachine:stm_launch_lambda",
                role_arn=f"arn:aws:iam::{str(config[stage]['awsAccountId'])}:role/service-role/Amazon_EventBridge_Scheduler_SFN_b61b2be1a1",
                input=json.dumps(self.schedule_input),
                retry_policy=scheduler.CfnSchedule.RetryPolicyProperty(
                    maximum_event_age_in_seconds=900,
                    maximum_retry_attempts=0
                )
            ),

            description="",
            group_name="default",
            name="import_schedule",
            schedule_expression_timezone="America/Bogota",
            state="DISABLED"
        )
        self.import_schedule.apply_removal_policy(RemovalPolicy.RETAIN)

        