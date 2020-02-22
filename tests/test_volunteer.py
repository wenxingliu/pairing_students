import datetime as dt
from data_mapper import read_and_clean_volunteers
from models.time_slot import TimeSlot, TimeSlotList
from services.utils import compute_volunteers


VOLUNTEER_DF = read_and_clean_volunteers(xlsx_file_path_list=['volunteer'],
                                         sheet_name='Sheet1',
                                         data_dir='tests/mock_data')

volunteers = compute_volunteers(VOLUNTEER_DF)


def test_timezone_conversion():
    volunteer_1 = _find_volunteer('volunteer1')
    volunteer_2 = _find_volunteer('volunteer2')
    volunteer_4 = _find_volunteer('volunteer4')

    volunteer_1_time_slots = [
        TimeSlot(start=dt.datetime(2001, 1, 1, 22), end=dt.datetime(2001, 1, 1, 22, 30), weekday=5),
        TimeSlot(start=dt.datetime(2001, 1, 1, 10, 30), end=dt.datetime(2001, 1, 1, 11), weekday=0),
    ]

    assert volunteer_1.time_slots_china == TimeSlotList(volunteer_1_time_slots)

    volunteer_2_time_slots = [
        TimeSlot(start=dt.datetime(2001, 1, 1, 12, 30), end=dt.datetime(2001, 1, 1, 13), weekday=5)
    ]

    assert volunteer_2.time_slots_china == TimeSlotList(volunteer_2_time_slots)


def _find_volunteer(name):
    for v in volunteers:
        if v.name == name:
            return v


test_timezone_conversion()