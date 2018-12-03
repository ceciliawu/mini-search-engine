__author__ = 'Si Yi Wu'


import boto.ec2
import time
import aws_setup

# define some constants
KEY_NAME = 'greenlight'
SECURITY_GROUP_NAME = 'csc326_group26'
IMAGE_ID = 'ami-8caa1ce4'


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

def create_aws_instance(awsKeyId,awsSecretAccessKey):
    #establish connection to amazon
    awsConnection = boto.ec2.connect_to_region ("us-east-1",aws_access_key_id=awsKeyId,aws_secret_access_key=awsSecretAccessKey)
    print ("connection successfully established.\n")

    keyPair = awsConnection.create_key_pair(KEY_NAME, dry_run=False)
    keyPair.save("./")
    print("key pair created.\n")

    securityGroup = awsConnection.create_security_group(SECURITY_GROUP_NAME,'Security Group for Group 26')
    securityGroupName = securityGroup.name
    print ("security group named " + securityGroupName + " is created. \n")
    awsConnection.authorize_security_group(group_name = securityGroupName, ip_protocol= 'icmp' , from_port = -1, to_port= -1, cidr_ip = '0.0.0.0/0')
    awsConnection.authorize_security_group(group_name = securityGroupName, ip_protocol= 'tcp' , from_port = 22, to_port= 22, cidr_ip = '0.0.0.0/0')
    awsConnection.authorize_security_group(group_name = securityGroupName, ip_protocol= 'tcp' , from_port = 80, to_port= 80, cidr_ip = '0.0.0.0/0')
    print ("security group authorized\n")

    reservationObject = awsConnection.run_instances(image_id=IMAGE_ID,key_name=KEY_NAME,security_groups=[securityGroupName],instance_type='t1.micro')
    awsInstance = reservationObject.instances[0]

    print ("Please wait while the instance is being brought up\n")

    while (awsInstance.update()!='running'):
        time.sleep(3)

    instance_Id = awsInstance.id
    public_DNS = awsInstance.public_dns_name
    public_Ip = awsInstance.ip_address

    #wait for the instane to become stable
    print("the instance is up and running now but please wait while it initializes and stablizes\n")
    status = 'not_ready'
    while (status != 'ok'):
        time.sleep(3)
        instances = awsConnection.get_all_instance_status(instance_ids=instance_Id)
        status = 'not_ready'
        if instances:
            status = instances[0].system_status.status
    print ("instance ready\n")
    return instance_Id,public_DNS,public_Ip

def modify_frontend(public_Ip):
    with open('./FrontEnd/FrontEnd.py', 'r') as FE1:
        line = FE1.readlines()
        replace_line = "baseURL = 'http://ec2-" + public_Ip.replace('.','-')+".compute-1.amazonaws.com'\n"
        line[15] = replace_line
        FE1.close()
    with open('./FrontEnd/FrontEnd.py', 'w') as FE2:
        FE2.writelines(line)
        FE2.close()



if __name__ == "__main__":
    # first get the credentials from a separate credential file
    awsKeyId,awsSecretAccessKey = get_aws_credentials()

    # create an aws instance and get the necessary information
    instance_Id,public_DNS,public_Ip = create_aws_instance(awsKeyId,awsSecretAccessKey)

    # modify the FrontEnd.py to replace the DNS address
    modify_frontend(public_Ip)

    # set up the aws for deployment
    aws_setup.aws_setup(public_DNS,str(public_Ip))

    # after we return from the previous function, it's completed
    print ("The website has been successfully set up, please access using the following: \n")
    print("Public DNS is: " + public_DNS + "\n")
    print("Public IP is: " + public_Ip + "\n")
    print("The instance ID is: " + instance_Id + ". Please use this to terminate the instance. \n")



