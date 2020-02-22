import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from typing import List

from secrets.private import GMAIL_ACCOUNT, GMAIL_PASSWORD
from models.volunteer import Volunteer


def email_to_all_volunteers(all_volunteers: List[Volunteer]):
    for volunteer in all_volunteers:
        if volunteer.paired_student or volunteer.recommendation_filled:
            send_email(volunteer)


def send_email_to_volunteer(volunteer: Volunteer):
    subject = "Communities Without Boundaries Foundation: Your friend in China is waiting!"
    send_to = [volunteer.volunteer_email, volunteer.parent_email]
    text = _compute_text(volunteer)

    send_email(subject=subject, text=text, send_to=send_to)


def send_email(subject,
               text,
               send_to,
               send_from=GMAIL_ACCOUNT,
               username=GMAIL_ACCOUNT,
               password=GMAIL_PASSWORD,
               file=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
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
        print('successfully sent the email')
    except:
        print("failed to send email")


def _compute_text(volunteer: Volunteer) -> str:
    if volunteer.paired_student:
        text = _compute_text_of_assigned_volunteer(volunteer)
    else:
        text = _compute_text_of_unassigned_volunteer(volunteer)
    return text


def _compute_text_of_assigned_volunteer(volunteer: Volunteer) -> str:

    student_info = ""
    for student in volunteer.paired_student:
        student_info += student.formatted_info

    body_text = f"""
    Hi {volunteer.name.title()},

    Here is your matched results:

    {student_info}
    """

    return body_text


def _compute_text_of_unassigned_volunteer(volunteer: Volunteer) -> str:
    student_info = ""
    for student in volunteer.potential_match:
        student_info += student.formatted_info

    body_text = f"""
    Hi {volunteer.name.title()},

    Sorry, we were unable to accommodate the time you submitted. 
    For your reference, here are your selected time slots in your local time {volunteer.timezone}:
    
    {volunteer.time_slots_local}
    
    The converted Beijing time are:
    
    {volunteer.time_slots_china}
    
    Here are some potential match, please consider resubmit your time accordingly to get a match:

    {student_info}
    """

    return body_text
