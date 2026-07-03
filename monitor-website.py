import smtplib
import requests
import os

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

def send_notification(email_message):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: SITE DOWN\n{email_message}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)

try:
    response = requests.get("http://172-104-159-33.ip.linodeusercontent.com:8080/")
    if response.status_code == 200:
        print("Application is running successfully")
    else:
        print("Application down. You have to fix it. ")
        # send email to me.     T
        msg = f"Application returned {response.status_code}."
        send_notification(msg)

except Exception as ex:
    print(f"Connection Error. {ex}")
    msg = "Application is not accessible at all"
    send_notification(msg)