from models.volunteer import Volunteer


def compute_subject() -> str:
    return f"From Communities Without Boundaries Foundation: Your friend in China is waiting!"


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

    body_test = f"""
    Hi {volunteer.name.title()},

    {notification_text}
    """

    if volunteer.no_org:
        body_test += f"""If you are not in any wechat group, please scan the attached barcode to join. Thank you!"""

    return body_test


def _compute_text_of_assigned_volunteer(volunteer: Volunteer) -> str:

    student_info = ""
    for student in volunteer.paired_student:
        student_info += student.formatted_info

    body_text = f"""
    Here is a little bit more about your friend in China:
    {student_info}
    """

    return body_text


def _compute_text_of_unassigned_volunteer(volunteer: Volunteer) -> str:

    body_text = f"""
    Sorry, we were unable to accommodate the time you submitted. For your reference, here are your selected time slots in your local time {volunteer.timezone}:
    
    {time_slot_list_to_str_formatting(volunteer.time_slots_local)}
    
    The converted Beijing time are:
    
    {time_slot_list_to_str_formatting(volunteer.time_slots_china)}
    """

    student_info = ""
    for student in volunteer.potential_match:
        student_info += student.formatted_info

    if student_info:
        body_text += f"""
        Here are some potential fits, please consider resubmit time slots accordingly to help us get you a fit:
    
        {student_info}
        """
    else:
        body_text += """
        Please consider resubmit your time accordingly to get a successful match.
        """

    return body_text


def time_slot_list_to_str_formatting(time_slot_list) -> str:
    time_slot_str_list = [str(slot) for slot in time_slot_list]
    return ' ,'.join(time_slot_str_list)


def valid_email_address(email_address: str) -> bool:
    return '@' in str(email_address)
