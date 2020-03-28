import pandas as pd
import settings as settings


def read_volunteer_hours_df(volunteer_hours_file):

    df = pd.read_excel(f'{settings.CERTIFICATE_DIR}/{volunteer_hours_file}.xlsx',
                       sheet_name='Form Responses 1')

    df.rename(columns=settings.VOLUNTEER_HOURS_COLUMNS, inplace=True)
    df = df[list(settings.VOLUNTEER_HOURS_COLUMNS.values())]

    df.dropna(inplace=True)
    df.drop_duplicates(['volunteer'], keep='last', inplace=True)
    df['hours'] = df.hours.astype(int).astype(str)
    df['volunteer'] = df.volunteer.apply(lambda n: n.title())

    return df
