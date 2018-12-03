__author__ = 'Si Yi Wu'


import boto.ec2
import os
import time

AWS_KEY_ID = 'AKIAJWKFMXPDMTABNXUA'
AWS_SECRET_ACCESS_KEY = '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'
KEY_NAME = 'greenLight'
SECURITY_GROUP_NAME = 'csc326-group26'
IMAGE_ID = 'ami-8caa1ce4'


#establish connection to amazon
awsConnection = boto.ec2.connect_to_region ("us-east-1",aws_access_key_id=AWS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
print ("connection successfully established.\n")




keyPair = awsConnection.create_key_pair(KEY_NAME, dry_run=False)
keyPair.save("./")
print("key pair created.\n")


securityGroup = awsConnection.create_security_group(SECURITY_GROUP_NAME,'Security Group for Group 26')
print("security group created.\n")

securityGroupName = securityGroup.name
print (securityGroupName)
awsConnection.authorize_security_group(group_name = securityGroupName, ip_protocol= 'icmp' , from_port = -1, to_port= -1, cidr_ip = '0.0.0.0/0')
awsConnection.authorize_security_group(group_name = securityGroupName, ip_protocol= 'tcp' , from_port = 22, to_port= 22, cidr_ip = '0.0.0.0/0')
awsConnection.authorize_security_group(group_name = securityGroupName, ip_protocol= 'tcp' , from_port = 80, to_port= 80, cidr_ip = '0.0.0.0/0')

print ("security group authorized\n")

reservationObject = awsConnection.run_instances(image_id=IMAGE_ID,key_name=KEY_NAME,security_groups=[securityGroupName],instance_type='t1.micro')
awsInstance = reservationObject.instances[0]

#wait for the instane to be stable
print (awsInstance.update())
while (awsInstance.update()!='running'):
    time.sleep(3)

print ("instance ready")

#associate an elastic IP address with the instance
elasticIPAddress = awsConnection.allocate_address()
elasticIPAddress.associate(instance_id=awsInstance.id)
print (elasticIPAddress)

