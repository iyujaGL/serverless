import json
from boto3 import client
from botocore.exceptions import ClientError


def reboot(event, context):

    stack_name = event['stack']
    cfn = client('cloudformation')
    asg = client('autoscaling')
    ec2 = client('ec2')


    try:
        print("Listing resources in: ", stack_name)

        stack_resources = cfn.list_stack_resources(
            StackName=stack_name
        )['StackResourceSummaries']

    except ClientError as e:
        message = e.response['Error']


    asg_list = []


    try:
        for resource in stack_resources:
            if resource['ResourceType'] == "AWS::AutoScaling::AutoScalingGroup":
                print("Found AutoScalingGroup: ", resource['PhysicalResourceId'])
                asg_list.append(resource['PhysicalResourceId'])

    except ClientError as e:
        message = e.response['Error']


    try:
        autoscaling_groups = asg.describe_auto_scaling_groups(
            AutoScalingGroupNames=asg_list
        )['AutoScalingGroups']

        for autoscaling_group in autoscaling_groups:
            instance_id_list = [instance['InstanceId'] for instance in autoscaling_group['Instances']]

            print("Rebooting instances: ", instance_id_list)

            ec2.reboot_instances(
                InstanceIds=instance_id_list,
                DryRun=event['dryrun']
            )
            message = 'Instances: ' + ''.join(instance_id_list) + ' rebooted'

    except ClientError as e:
        message = e.response['Error']


    body = {
        "message": message
    }


    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
