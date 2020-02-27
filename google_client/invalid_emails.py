from data.invalid_email_list import invalid_emails


def valid_email_address(email_address: str) -> bool:
    is_email = '@' in str(email_address)
    is_valid = str(email_address).lower() not in invalid_emails
    return is_email and is_valid
