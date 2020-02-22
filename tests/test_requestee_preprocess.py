import datetime as dt
from data_mapper import read_and_clean_requests
from models.time_slot import TimeSlot, TimeSlotList

REQUEST_DF = read_and_clean_requests(xlsx_file_path='tests/mock_data/requestee.xlsx',
                                     sheet_name='学生信息收集表')


def test_requestee_data_deduplicate():
    unique_requests = sorted(REQUEST_DF.requestee.tolist())
    expected_unique_requests = ["test_requestee1", "test_requestee2", "test_requestee3",
                                "test_requestee4", "test_requestee5"]
    assert unique_requests == expected_unique_requests


def test_take_latest_record():
    duplicate_request = REQUEST_DF.loc[REQUEST_DF.requestee == 'test_requestee3'].reset_index().T.to_dict()[0]
    computed_time_slots = duplicate_request['time_slots_china']

    expected_time_slot = TimeSlot(start=dt.datetime(2001, 1, 1, 10, 30),
                                  end=dt.datetime(2001, 1, 1, 11),
                                  weekday=2)
    expected_time_slots = TimeSlotList([expected_time_slot])

    assert computed_time_slots == expected_time_slots


def test_time_slots_calculation():
    selected_request = REQUEST_DF.loc[REQUEST_DF.requestee == 'test_requestee5'].reset_index().T.to_dict()[0]
    expected_time_slots_china = [
        TimeSlot(start=dt.datetime(2001, 1, 1, 11), end=dt.datetime(2001, 1, 1, 11, 30), weekday=5),
        TimeSlot(start=dt.datetime(2001, 1, 1, 21, 30), end=dt.datetime(2001, 1, 1, 22), weekday=5),
        TimeSlot(start=dt.datetime(2001, 1, 1, 22), end=dt.datetime(2001, 1, 1, 22, 30), weekday=5)
    ]

    assert selected_request['time_slots_china'] == TimeSlotList(expected_time_slots_china)


test_requestee_data_deduplicate()
test_take_latest_record()
test_time_slots_calculation()
