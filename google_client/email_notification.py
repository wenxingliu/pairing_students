import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders


def send_email(subject,
               text,
               send_to,
               send_from,
               username,
               password,
               file=None,
               server="smtp.gmail.com",
               port=587,
               isTls=True):
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

        smtp = smtplib.SMTP(server, port)
        if isTls:
            smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()
        print('successfully sent the email')
    except:
        print("failed to send email")


def send_email_with_html(subject,
                         send_to,
                         send_from,
                         username,
                         password,
                         html='',
                         file=None,
                         server="smtp.gmail.com",
                         port=587,
                         isTls=True):
    try:
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = ", ".join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(html, 'html'))

        part = MIMEBase('application', "octet-stream")
        if file is not None:
            part.set_payload(open(file, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
            msg.attach(part)

        smtp = smtplib.SMTP(server, port)
        if isTls:
            smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.quit()
        print('successfully sent the email')
    except:
        print("failed to send email")
