# DevOps Python Automation
program checks if the response status on HTTP request is 200, if not it initiates a restart of nginx application container.
in case the request gets an error response, programs reboots the server and restarts the container
program uses Linode client to access the remote virtual machine on Linode platform. For this purpose the library linode_api4 is imported.
To execute linux commands on virtual server the SSH client is defined by using paramiko library
User is notified by an email that is being sent through smtplib library
environmental variables as EMAIL_ADDRESS, EMAIL_PASSWORD and LINODE_TOKEN can be defined in Linux by export command: example: export EMAIL_ADDRESS = value
