import smtplib
import linode_api4
import requests
import os
import paramiko
import time
import schedule


EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
LINODE_TOKEN = os.environ.get("LINODE_TOKEN")

def send_email_notification(email_message):
    print("Sending notification ...")
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n{email_message}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)


def restart_container():
    print("Restarting container ...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='172.104.159.33', username='root', key_filename='/home/petr-ubuntu/.ssh/id_rsa', port=22)
    stdin, stdout, stderr = ssh.exec_command('docker start 3dbdef96df34')
    print(stdout.readlines())
    ssh.close()
    print("Application has been restarted.")


def restart_server_and_container():
    print("Rebooting the server ... ")
    client = linode_api4.LinodeClient(LINODE_TOKEN)
    nginx_server = client.load(linode_api4.Instance, 100227968)
    nginx_server.reboot()

    #restart the application
    while True:
        nginx_server = client.load(linode_api4.Instance, 100227968)
        if nginx_server.status == 'running':
            time.sleep(15)
            restart_container()
            break

def monitor_application():
    try:
        response = requests.get("http://172-104-159-33.ip.linodeusercontent.com:8080/")
        if response.status_code == 200:
            print("Application is running successfully")
        else:
            print("Application down. You have to fix it. ")
            # send email to me.     T
            msg = f"Application returned {response.status_code}."
            send_email_notification(msg)
            # restart the application
            restart_container()

    except Exception as ex:
        print(f"Connection Error. {ex}")
        msg = "Application is not accessible at all"
        send_email_notification(msg)
        #restart linode server and container
        restart_server_and_container()

schedule.every(5).seconds.do(monitor_application)

while True:
    schedule.run_pending()