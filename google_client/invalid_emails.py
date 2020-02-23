import pandas as pd
import settings


def _get_invalid_email_list():
    invalid_email_df = pd.read_csv(settings.INVALID_EMAIL_LIST_PATH)
    invalid_email_list = invalid_email_df.email.tolist()
    invalid_email_list = [email_addr.lower() for email_addr in invalid_email_list]
    return invalid_email_list


def valid_email_address(email_address: str) -> bool:
    is_email = '@' in str(email_address)
    invalid = str(email_address).lower() in INVALID_EMAIL
    return is_email and (not invalid)


INVALID_EMAIL = _get_invalid_email_list()


