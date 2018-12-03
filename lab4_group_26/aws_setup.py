__author__ = 'Si Yi Wu'

import paramiko
import os

KEY_FILE_NAME = 'greenlight.pem'

def aws_setup (public_DNS,public_IP):
    #first scp the files needed to the IP address
    IP_connection = "ubuntu@" + public_IP
    print public_IP
    print IP_connection
    os.system("scp -o StrictHostKeyChecking=no -i " + KEY_FILE_NAME + " -r FrontEnd/ " + IP_connection + ":~/")

    #now create an ssh session to connect to the remote aws instance
    primary_key = paramiko.RSAKey.from_private_key_file(KEY_FILE_NAME)
    aws_connection = paramiko.SSHClient()
    aws_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    aws_connection.connect( hostname=public_DNS,username='ubuntu',pkey=primary_key)

    #a series of commands to run on the aws instance
    commands = [
                 "sudo apt-get update",
                 "sudo apt-get install -y python-pip",
                 "sudo pip install bottle",
                 "sudo pip install httplib2",
                 "sudo pip install beaker",
                 "cd FrontEnd; sudo nohup python FrontEnd.py  > /dev/null 2>&1 &"
                ]

    for command in commands:
        print "Executing {}".format( command )
        stdin , stdout, stderr = aws_connection.exec_command(command) # this command is executed on the *remote* server
        print stdout.read()
        error_message = stderr.read()
        if (error_message):
            print("Errors:")
            print error_message
        print ("------------------------------")

    aws_connection.close()
    return




