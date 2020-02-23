from models.volunteer import Volunteer


def compute_subject() -> str:
    return f"From Communities Without Boundaries Foundation: \
Your friend in China is waiting!"


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
    else:
        notification_text = _compute_text_of_unassigned_volunteer(volunteer)

    org_reminder_text = _compute_no_org_reminder_text(volunteer)
    last_paragraph = _closing_paragraph()

    body_test = f"""
Hi {volunteer.name.title()},
{notification_text}
{org_reminder_text}{last_paragraph}
    """

    return body_test


def _closing_paragraph():
    return f"""
One last thing... Please keep in mind the Daylight Saving change on Mar 8th when scheduling.
    """


def _compute_no_org_reminder_text(volunteer: Volunteer):
    reminder_text = ""
    if volunteer.no_org:
        reminder_text = f"""
P.S. If you are not in a wechat group of any organization, please scan the attached barcode to join. \
Most of our communications will happen in wechat group. Thank you!
    """
    return reminder_text


def _compute_text_of_assigned_volunteer(volunteer: Volunteer) -> str:

    student_info = ""
    for student in volunteer.paired_student:
        student_info += student.formatted_info

    body_text = f"""
Here is a little bit more about your friend in China:
    {student_info}"""

    return body_text


def _compute_text_of_unassigned_volunteer(volunteer: Volunteer) -> str:

    body_text = f"""
We sincerely apologize for not being able to accommodate the time you submitted. \
Please consider re-submit your time accordingly to get a successful match.

For your reference, here are your selected time slots in your local timezone \
({volunteer.timezone}):
{time_slot_list_to_str_formatting(volunteer.time_slots_local)}

The converted Beijing time are:
{time_slot_list_to_str_formatting(volunteer.time_slots_china)}
"""

    student_info = ""
    for student in volunteer.potential_match:
        student_info += student.formatted_info

    if student_info:
        body_text += f"""
Although we were not able to find a best fit, there are some possible time slots, \
please consider resubmit your available time slots accordingly to help us get you a fit:
    {student_info}"""
    return body_text


def time_slot_list_to_str_formatting(time_slot_list) -> str:
    time_slot_str_list = [str(slot) for slot in time_slot_list]
    return '\n'.join(time_slot_str_list)


def valid_email_address(email_address: str) -> bool:
    return '@' in str(email_address)
