import json
from boto3 import client
from botocore.exceptions import ClientError


def reboot(event, context):

    stackName = event['stack']
    cfn = client('cloudformation')
    asg = client('autoscaling')
    ec2 = client('ec2')

    asgName = cfn.describe_stack_resources(
                StackName=stackName,
                LogicalResourceId="appAsg"
            )['StackResources'][0]['PhysicalResourceId']

    asgInstances = asg.describe_auto_scaling_groups(
                AutoScalingGroupNames=[
                        asgName,
                    ]
            )['AutoScalingGroups'][0]['Instances']

    instanceIdList = [instance['InstanceId'] for instance in asgInstances]

    ec2.reboot_instances(
            InstanceIds=instanceIdList,
            DryRun=False
            )

    body = { 
        "message": "reboot successful"        
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
