import boto3
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


iam_client = boto3.client('iam')
# Specify region if running locally and ensure sender email is verified in SES
ses_client = boto3.client('ses', region_name='us-east-1')

expiry_days = 18
reminder_days = 5
reminder_email_age = expiry_days - reminder_days
username = "DevOps"
To_email = "16weeksofdevops@proton.me"
From_email =  "ideploy@proton.me"

# a function that get username as input, and return access keys and age 
def get_access_keys_age(username):
    try:
        response = iam_client.list_access_keys(
            UserName=username,
        ).get('AccessKeyMetadata', [])
    except iam_client.exceptions.NoSuchEntityException:
        print(f"User {username} does not exist.")
        return []
    except Exception as e:
        print(f"Error fetching access keys for {username}: {e}")
        return []

    access_keys_info = []
    for item in response:
        create_date = item['CreateDate']
        if isinstance(create_date, datetime.datetime):
            create_date = create_date.date()
        elif isinstance(create_date, datetime.date):
            create_date = create_date
        else:
            continue  # skip if create_date is not a date or datetime
        age = (datetime.date.today() - create_date).days
        access_key_id = item['AccessKeyId']
        access_keys_info.append((access_key_id, age))
    
    return access_keys_info

def if_key_expired(access_key_id, age, reminder_email_age):
    if age >= reminder_email_age:
        return f"Reminder: Access key {access_key_id} is {age} days old. Please rotate it."
    

def process_keys(username):
    access_keys_info = get_access_keys_age(username)
    reminders = []
    for access_key_id, age in access_keys_info:
        if age >= reminder_email_age:
            reminder = if_key_expired(access_key_id, age, reminder_email_age)
            if reminder:
                reminders.append(reminder)
    if reminders:
        return "\n".join(reminders)
    return "No access keys require rotation at this time."


# # send email funstion
# aws ses email
Subject = "Access Key Rotation Reminder"
Body = process_keys(username)


def build_email_message(to_email, from_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    body_part = MIMEText(body, 'plain')
    msg.attach(body_part)

    return msg

def send_email(msg, to_emails):
    response = ses_client.send_raw_email(
        Source=msg["From"],
        Destinations=to_emails,
        RawMessage={"Data": msg.as_string()}
    )
    return response

def lambda_handler(_event=None, _context=None):
    msg = build_email_message(To_email, From_email, Subject, Body)
    response = send_email(msg, [To_email])
    print(response)


# # while running locally, uncomment the following lines
# if __name__ == "__main__":
#     lambda_handler(None, None)