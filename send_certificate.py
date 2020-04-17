from data_mapper.volunteer_hours import read_volunteer_hours_df
from services.generate_certificate import generate_certificate
from google_client.email_notification import send_email
from secrets.private import GMAIL_ACCOUNT, GMAIL_PASSWORD
import settings as settings

from time import sleep


def generate_and_send_certificate(volunteer_hours_file: str,
                                  template_file: str,
                                  generate_doc: bool = True,
                                  email: bool = False):

    volunteer_df = read_volunteer_hours_df(volunteer_hours_file)

    for data_tuple in volunteer_df.itertuples():
        if generate_doc:
            generate_certificate(volunteer_name=data_tuple.volunteer,
                                 hours=data_tuple.hours,
                                 template_file=template_file)
            print(f'pandoc -s "{data_tuple.volunteer}.docx" -o "{data_tuple.volunteer}.pdf"')

        if email:
            try:
                subject = "Volunteer certificate (Virtual Teaching And Caring)"
                text = "Thank you for volunteering! Attached please find your volunteer hours certificate.\n\n- CWB Foundation"
                send_to = [data_tuple.email, data_tuple.parent_email]
                file_name = f"pdf/{data_tuple.volunteer}.pdf"
                file_path = f"{settings.CERTIFICATE_DIR}/{file_name}"

                send_email(subject=subject,
                           text=text,
                           send_to=send_to,
                           send_from=GMAIL_ACCOUNT,
                           username=GMAIL_ACCOUNT,
                           password=GMAIL_PASSWORD,
                           file=file_path)

                print(f"successfully sent to email {data_tuple.volunteer} at {data_tuple.email}")

                sleep(1)

            except:
                print(f"failed to email {data_tuple.volunteer} at {data_tuple.email}")


if __name__ == '__main__':
    # Step 1: Generate Files
    generate_and_send_certificate(volunteer_hours_file='volunteer_hours',
                                  template_file='Volunteer certificate-TEACHING-CARING',
                                  generate_doc=True,
                                  email=False)

    # Step 2: Convert to PDF

    # Step 3: Send PDFs
    # generate_and_send_certificate(volunteer_hours_file='volunteer_hours',
    #                               template_file='Volunteer certificate-TEACHING-CARING',
    #                               generate_doc=False,
    #                               email=True)
