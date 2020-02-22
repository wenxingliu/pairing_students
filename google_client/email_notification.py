import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from typing import List

from google_client import utils
from secrets.private import GMAIL_ACCOUNT, GMAIL_PASSWORD
from models.volunteer import Volunteer


def email_to_all_volunteers(all_volunteers: List[Volunteer]):
    for volunteer in all_volunteers:
        try:
            if volunteer.email_sent:
                print(f'Email already sent to {volunteer} at {volunteer.email_sent_time_utc}')
            else:
                send_email_to_volunteer(volunteer)
                volunteer.mark_email_sent()
                print(f'successfully sent email to {volunteer.name}')
        except:
            print(f'failed to send email to {volunteer.name} at \
            {volunteer.parent_email} or {volunteer.volunteer_email}')


def send_email_to_volunteer(volunteer: Volunteer):
    subject = utils.compute_subject()
    send_to = utils.compute_receiver(volunteer)

    if send_to:
        text = utils.compute_text(volunteer)
        send_email(subject=subject, text=text, send_to=send_to)
    else:
        print(f'{volunteer.name} no email address')


def send_email(subject,
               text,
               send_to,
               send_from=GMAIL_ACCOUNT,
               username=GMAIL_ACCOUNT,
               password=GMAIL_PASSWORD,
               file=None):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ','.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    if file is not None:
        part.set_payload(open(file, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
        msg.attach(part)

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(username, password)
    session.sendmail(send_from, send_to, msg.as_string())
    session.quit()
