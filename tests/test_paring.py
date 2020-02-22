from data_mapper import read_and_clean_requests, read_and_clean_volunteers
from utils.pairing import compute_requestees, compute_volunteers, pair_for_all

REQUEST_DF = read_and_clean_requests(xlsx_file_path='tests/mock_data/requestee.xlsx',
                                     sheet_name='学生信息收集表')

VOLUNTEER_DF = read_and_clean_volunteers(xlsx_file_path='tests/mock_data/volunteer.xlsx',
                                         sheet_name='Form Responses 1')

requestees = compute_requestees(REQUEST_DF)
volunteers = compute_volunteers(VOLUNTEER_DF)


def test_paring():
    sorted_requests = [request.name for request in requestees]
    expected_order = ["test_requestee1", "test_requestee5", "test_requestee3", "test_requestee4", "test_requestee2"]

    assert sorted_requests == expected_order

    pair_for_all(requestees, volunteers)

    target_volunteer = [volunteer for volunteer in volunteers if volunteer.name == 'volunteer4'][0]

    assert len(target_volunteer.paired_student) == 1
    assert target_volunteer.paired_student[0].name == 'test_requestee5'


test_paring()
