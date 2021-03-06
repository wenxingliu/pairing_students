from data.email_templates import (successful_email_chinese,
                                  failed_to_match_email_chinese,
                                  recommendation_email_chinese)
from google_client.invalid_emails import valid_email_address
from models.volunteer import Volunteer


def compute_subject(volunteer: Volunteer) -> str:
    if volunteer.paired_student:
        subject = """Online Tutoring For Students In China Project - We found you a match!"""
    else:
        subject = """Online Tutoring For Students In China Project - Attention Or Action Needed"""
    return subject


def compute_receiver(volunteer: Volunteer) -> str:
    receiver_list = []

    if valid_email_address(volunteer.parent_email):
        receiver_list.append(volunteer.parent_email)
    if valid_email_address(volunteer.volunteer_email):
        receiver_list.append(volunteer.volunteer_email)

    return receiver_list


def compute_text(volunteer: Volunteer) -> str:
    if volunteer.paired_student:
        notification_text = _compute_text_of_assigned_volunteer(volunteer)
        chinese_email = successful_email_chinese
    elif volunteer.recommendation_made:
        notification_text = _compute_text_of_volunteer_with_recommendation(volunteer)
        chinese_email = recommendation_email_chinese
    else:
        notification_text = _compute_text_of_unassigned_volunteer(volunteer)
        chinese_email = failed_to_match_email_chinese

    org_reminder_text = _compute_no_org_reminder_text(volunteer)
    last_paragraph = _closing_paragraph()

    body_test = f"""
Hi {volunteer.name.title()},

Thank you sincerely for joining the online tutoring/e-pal project for students in China. \
By building relationships with the students in China, you’re making a positive impact in \
their lives at a very challenging time.
{notification_text}
Tips and things to note:
1. We understand the importance of privacy to everyone involved. \
Please do NOT share the personal information of the student/parent to anyone else.      
2. Please find useful resources at the end of this email. \
(links shared by other volunteers, please use at your own discretion)
{org_reminder_text}
{last_paragraph}
{chinese_email}"""

    return body_test


def _next_steps_text():
    next_steps_text = f"""
Next steps:
1. Please reach out to your matched friend in China on WeChat. 
2. Please kindly inform the group leader of the organization you are with that you have \
successfully got in touch with your e-pal, or let them know if you have any questions. \
This is the last round of the matching process, \
if you have any issue getting in touch with the student and/or parent in China, \
please also let the group leader of your organization know. 
3. Mark your calendar for four tutoring/e-pal sessions in the following weeks."""
    return next_steps_text


def _compute_text_of_assigned_volunteer(volunteer: Volunteer) -> str:

    student_info = ""
    for student in volunteer.paired_student:
        student_info += student.formatted_info

    next_steps_text = _next_steps_text()

    body_text = f"""
We’re thrilled to tell you a little bit more about your friend(s) in China. \
    {student_info}
{next_steps_text}
"""

    return body_text


def _compute_text_of_volunteer_with_recommendation(volunteer: Volunteer) -> str:
    body_text = f"""
We, together with the students in China, \
are appreciative of the outpouring of your generosity around this project. \
We were unable to find an exact fit for you due to timezone differences, \
and we sincerely apologize for not being able to accommodate the time you selected.
    """

    student_info = ""
    for student in volunteer.potential_match:
        student_info += student.formatted_info

    if student_info:
        next_steps_text = _next_steps_text()
        body_text += f"""
Although we were not able to find a perfect time fit, \
we found someone who chose a similar time as you did. \
Please communicate with the student to schedule session time:
        {student_info}
    {next_steps_text}
"""

    return body_text


def _compute_text_of_unassigned_volunteer(volunteer: Volunteer) -> str:

    body_text = f"""
We, together with the students in China, \
are appreciative of the outpouring of your generosity around this project. \
We are very sorry that we were unable to find a good fit for you at this round \
due to time zone differences and other various reasons. \
You will automatically enter the next matching process.
The final round of matching will be at 12pm (Central Time) on March 1st. \
The final match result will also be sent to you via email.

Thank you very much for your support!
"""
    return body_text


def _compute_no_org_reminder_text(volunteer: Volunteer):
    reminder_text = ""
    if volunteer.no_org:
        reminder_text = f"""3. If you are not in a WeChat group of any organization, \
please scan the attached barcode to join. \
Most of our communications will happen in WeChat group."""
    return reminder_text


def _closing_paragraph():
    return f"""
One last thing... Please keep in mind *the Daylight Saving change on Mar 8th* when scheduling.
"""


def time_slot_list_to_str_formatting(time_slot_list) -> str:
    time_slot_str_list = [str(slot) for slot in time_slot_list]
    return '\n'.join(time_slot_str_list)


