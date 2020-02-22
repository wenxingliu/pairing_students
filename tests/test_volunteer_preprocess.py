import datetime as dt
from data_mapper import read_and_clean_volunteers
from models.time_slot import TimeSlot, TimeSlotList

VOLUNTEER_DF = read_and_clean_volunteers(xlsx_file_path_list=['volunteer'],
                                         sheet_name='Sheet1',
                                         data_dir='tests/mock_data')


def test_volunteer_data_deduplicate():
    unique_volunteers = sorted(VOLUNTEER_DF.name.tolist())
    expected_unique_volunteers = ["volunteer1", "volunteer2", "volunteer3", "volunteer4"]
    assert unique_volunteers == expected_unique_volunteers


def test_take_latest_record():
    duplicate_request = VOLUNTEER_DF.loc[VOLUNTEER_DF.name == 'volunteer1'].reset_index().T.to_dict()[0]
    computed_time_slots = duplicate_request['time_slots_local']

    expected_time_slot_1 = TimeSlot(start=dt.datetime(2001, 1, 1, 8),
                                    end=dt.datetime(2001, 1, 1, 8, 30),
                                    weekday=5)

    expected_time_slot_2 = TimeSlot(start=dt.datetime(2001, 1, 1, 8, 30),
                                    end=dt.datetime(2001, 1, 1, 9),
                                    weekday=6)

    expected_time_slots = TimeSlotList([expected_time_slot_1, expected_time_slot_2])

    assert computed_time_slots == expected_time_slots


test_volunteer_data_deduplicate()
test_take_latest_record()
