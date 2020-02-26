from google_client.invalid_emails import valid_email_address
from models.volunteer import Volunteer


def compute_subject(volunteer: Volunteer) -> str:
    if volunteer.paired_student:
        subject = """[Online Tutoring For Students In China Project] - We found you a match!"""
    else:
        subject = """[Online Tutoring For Students In China Project] - Attention Or Action Needed"""
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
    elif volunteer.recommendation_made:
        notification_text = _compute_text_of_volunteer_with_recommendation(volunteer)
    else:
        notification_text = _compute_text_of_unassigned_volunteer(volunteer)

    org_reminder_text = _compute_no_org_reminder_text(volunteer)
    last_paragraph = _closing_paragraph()

    body_test = f"""
Hi {volunteer.name.title()},

Thank you sincerely for joining the online tutoring/e-pal project for students in China. \
By building relationships with the students in China, you’re making a positive impact in \
their lives at a very challenging time.
{notification_text}
{org_reminder_text}{last_paragraph}
    """

    return body_test


def _next_steps_text():
    next_steps_text = f"""
Next steps:
1. Please reach out to your matched friend in China on Wechat. 
2. Please kindly inform the group leader of the organization you are with that you have \
successfully got in touch with your e-pal, or let them know if you have any questions.
3. Four (or more) tutoring/e-pal sessions between 2/29 - 3/28 in your assigned times."""
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
Although there are many students waiting to be connected. \
we were unable to find an exact fit for you due to timezone differences, \
We sincerely apologize for not being able to accommodate the time you selected.
    """

    student_info = ""
    for student in volunteer.potential_match:
        student_info += student.formatted_info

    if student_info:
        next_steps_text = _next_steps_text()
        body_text += f"""
Although we were not able to find a perfect fit, we found a potential match for you:
        {student_info}
    {next_steps_text}"""

    return body_text


def _compute_text_of_unassigned_volunteer(volunteer: Volunteer) -> str:

    body_text = f"""
We, together with the students in China, \
are appreciative of the outpouring of your generosity around this project. \
Although there are many students waiting to be connected. \
we were unable to find a good fit for you due to timezone differences, \
We sincerely apologize for not being able to accommodate the time you selected. \
Please kindly consider re-submitting a form through the following link, \
and try a different time to help us connect you with a friend in China.

https://forms.gle/CKiQGz58CdU3hUXz7

For your reference, here are your selected time slots in your local timezone \
({volunteer.timezone}):
{time_slot_list_to_str_formatting(volunteer.time_slots_local)}

The converted Beijing time are:
{time_slot_list_to_str_formatting(volunteer.time_slots_china)}
"""
    return body_text


def _compute_no_org_reminder_text(volunteer: Volunteer):
    reminder_text = ""
    if volunteer.no_org:
        reminder_text = f"""P.S. If you are not in a Wechat group of any organization, \
please scan the attached barcode to join. \
Most of our communications will happen in Wechat group. Thank you!
    """
    return reminder_text


def _closing_paragraph():
    return f"""
One last thing... Please keep in mind *the Daylight Saving change on Mar 8th* when scheduling."""


def time_slot_list_to_str_formatting(time_slot_list) -> str:
    time_slot_str_list = [str(slot) for slot in time_slot_list]
    return '\n'.join(time_slot_str_list)


