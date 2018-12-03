__author__ = 'Si Yi Wu'

import boto.ec2
import os
import sys
import time

KEY_NAME = 'greenlight'
SECURITY_GROUP_NAME = 'group26'

# read aws credentials from a seperate credential files
def get_aws_credentials():

    credentials = {}
    with open ("aws_credentials.txt") as credential_file:
        for line in credential_file:
            line = line.rstrip('\n')
            credentialType,credentialValue = line.partition("=")[::2]
            credentials[credentialType]=credentialValue
    awsKeyId = credentials['AWS_KEY_ID']
    awsSecretAccessKey = credentials['AWS_SECRET_ACCESS_KEY']
    return (awsKeyId,awsSecretAccessKey)

def delete_key_pair_security_group(awsConnection):
    #delete any previously created key pairs with the key name
    awsConnection.delete_key_pair(KEY_NAME, dry_run=False)
    os.system("rm -f %s"  % './' + KEY_NAME+'.pem')
    print ("key_pair " + KEY_NAME + " deleted successfully.  \n")


def terminate_instance(awsKeyId,awsSecretAccessKey,instanceId):
    #establish connection to amazon
    awsConnection = boto.ec2.connect_to_region ("us-east-1",aws_access_key_id=awsKeyId,aws_secret_access_key=awsSecretAccessKey)
    print ("connection successfully established.\n")

    awsConnection.terminate_instances(instance_ids = [instanceId])

    #check if the instance has been successfully terminated
    if (not awsConnection.get_all_instance_status(instance_ids=instanceId)):
        print ("aws instance successfully terminated.\n")
        return awsConnection
    else:
        print("oops there's sth wrong while terminating the instance.\n ")
        sys.exit(1)


if __name__ == "__main__":
    try:
        instanceId = sys.argv[1]
    except Exception,e:
        print "Please enter an instance Id\n"
        raise
        sys.exit(1)

    awsKeyId,awsSecretAccessKey = get_aws_credentials()
    awsConnection = terminate_instance(awsKeyId,awsSecretAccessKey,instanceId)
    delete_key_pair_security_group(awsConnection)