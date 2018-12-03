__author__ = 'Si Yi Wu'

import boto.ec2
import os

AWS_KEY_ID = 'AKIAJWKFMXPDMTABNXUA'
AWS_SECRET_ACCESS_KEY = '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'
KEY_NAME = 'greenLight'
SECURITY_GROUP_NAME = 'csc326-group26'


#establish connection to amazon
awsConnection = boto.ec2.connect_to_region ("us-east-1",aws_access_key_id=AWS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
print ("connection successfully established.\n")



#delete any previously created key pairs with the key name
awsConnection.delete_key_pair(KEY_NAME, dry_run=False)
os.system("rm -f %s"  % './' + KEY_NAME+'.pem')
print ("key_pair deleted successfully.\n")


#delete any existing security group with same name
awsConnection.delete_security_group(name=SECURITY_GROUP_NAME)
print ("security group deleted successfully.\n")
