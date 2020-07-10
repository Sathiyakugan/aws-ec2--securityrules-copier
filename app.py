import json

import boto3
from botocore.exceptions import ClientError


def get_existing_security_group_id():
    return input("Please enter the Existing security groupId you wanted to copy: \n")


def get_target_security_group_id():
    return input("Please enter the Target security groupId you wanted to copy: \n")


def print_error_and_exit(msg):
    print(msg)
    exit()


def read_config(file_name):
    # Load the config file.
    try:
        with open('conf/config.json', 'r') as f:
            config = json.load(f)
            return config
    except IOError:
        print_error_and_exit("Could not read file: " + file_name)


def main():
    # Load the config file.
    file_name = 'conf/config.json'
    config = read_config(file_name)

    print("Hi,  Welcome to the AWS EC2 security-rules Copier....\n")

    aws_access_key_id = config['ACCESS_KEY']
    aws_secret_access_key = config['SECRET_KEY']
    region_name = config['REGION_NAME']

    # Checking whether the default value is changed.
    if aws_access_key_id == 'ACCESS_KEY' or aws_secret_access_key == 'SECRET_KEY' or region_name == 'REGION_NAME':
        print_error_and_exit("Hey, you forgot to add the config to the \"conf/config.json\" . Please add " +
                             "and restart the app.")


    # getting the ec2 resource.
    ec2 = boto3.resource(
        'ec2',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    # Defining the necessary variables.
    success = False
    is_valid_existing_security_group_id = False

    existing_security_group_res_ip = None
    existing_security_group_res_ip_egress = None

    while not success:
        try:
            # getting the rules of the existing security group
            if not is_valid_existing_security_group_id:
                existing_security_group_id = get_existing_security_group_id()
                existing_security_group_res = ec2.SecurityGroup(existing_security_group_id)
                existing_security_group_res_ip = existing_security_group_res.ip_permissions
                existing_security_group_res_ip_egress = existing_security_group_res.ip_permissions_egress
                is_valid_existing_security_group_id = True

            # getting the rules of the target security group
            target_security_group_id = get_target_security_group_id()
            target_security_group_res = ec2.SecurityGroup(target_security_group_id)
            current_ip_permission = target_security_group_res.ip_permissions

            # revoking existing rules.
            if len(current_ip_permission) > 0:
                cur_res = target_security_group_res.revoke_ingress(IpPermissions=current_ip_permission)
                if cur_res['ResponseMetadata']['HTTPStatusCode'] != 200:
                    print_error_and_exit(
                        "You don't have the required permissions to revoke_ingress of the security group.")
            # revoking existing rules.
            current_permissions_egress = target_security_group_res.ip_permissions_egress
            if len(current_permissions_egress) > 0:
                cur_res = target_security_group_res.revoke_egress(IpPermissions=current_permissions_egress)
                if cur_res['ResponseMetadata']['HTTPStatusCode'] != 200:
                    print_error_and_exit("You don't have the required permissions to " +
                                         "revoke_egress of target security group.")
            # setting new rules.
            cur_res = target_security_group_res.authorize_ingress(IpPermissions=existing_security_group_res_ip)
            if cur_res['ResponseMetadata']['HTTPStatusCode'] != 200:
                print_error_and_exit(" You don't have the required permissions to add Inbound rules of target" +
                                     " security group.")
            # setting new rules.
            cur_res = target_security_group_res.authorize_egress(IpPermissions=existing_security_group_res_ip_egress)
            if cur_res['ResponseMetadata']['HTTPStatusCode'] != 200:
                print_error_and_exit(" You don't have the required permissions to add Inbound rules of "
                                     "target security group.")

            success = True
            print("You have successfully updated the security rules of the id to : " + target_security_group_id +
                  " from : " + existing_security_group_id)

        except ClientError as err:
            if err.response['Error']['Code'] == 'AuthFailure':
                print_error_and_exit("Please make sure you have added the valid credential to the config file.")
            if err.response['Error']['Code'] == 'InvalidGroupId.Malformed' and not is_valid_existing_security_group_id:
                print("You have given wrong Existing security groupId. Please make sure it is correct and retry. \n")
                continue
            if err.response['Error']['Code'] == 'InvalidGroupId.Malformed':
                print("You have given wrong Existing security groupId. Please make sure it is correct and retry. \n")
                continue
            else:
                print_error_and_exit("There was an unexpected Error occurred in our program. Please try again later.")


if __name__ == "__main__":
    main()
