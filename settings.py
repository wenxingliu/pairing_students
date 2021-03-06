REQUEST_COLUMNS_MAPPER = {
    "提交时间（自动）": "timestamp",
    "提交者（自动）": "requestee",
    "家长微信号（必填）": "parent_wechat",
    "孩子性别（必填）": "gender",
    "孩子年龄（必填）": "age_raw",
    "孩子学习英文几年（必填）": "english_learning_in_years",
    "选择教学时间（必填）": "time_slot_day",
    "选择教学时间段（必填）": "time_slot_time",
    "教学交流内容（必填）": "content",
    "希望视频教学交流学生的性别（必填）": "volunteer_gender",
    "家长是否有一方是医护人员？（必填）": "doctor_family",
    "孩子是否是病患子女？（必填）": "patient_family",
    # latest form new cols
    "家长手机号码（必填）": "parent_phone",
    "家长电子信箱地址（必填）": "parent_email",
    "孩子姓名（必填）": "name",
    "家长是否有一方是医护人员？或者孩子是否是病患子女？（必填）": "doctor_family",
    "是否在武汉或者湖北其他地区？（必填）": "hubei_family"
}

VOLUNTEER_COLUMNS_MAPPER = {
    "Timestamp": "timestamp",
    "Volunteers Name": "name",
    "Volunteers Email": "volunteer_email",
    "Parents name": "parent",
    "Parents Email": "parent_email",
    "Parents Wechat ID": "parent_wechat",
    "Volunteers age": "age",
    "Volunteers gender": "volunteer_gender",
    "Volunteers local time zone": "timezone",
    "Where did you learn about this event?": "organization",
    "Teaching content you are interested in [You can choose one or more]": "content",
    "How many students do you want to teach per week? (30 minutes of teaching per student per week)": "num_pairs"
}

CONFIRMATION_COLUMNS_MAPPER = {
    "email received (check box for yes, leave blank for no)": "email_received",
    "accept matching result (check box for yes, leave blank for no)": "accept_pairing",
    "is able to connect with student in china using their wechat ID (check box for yes, leave blank for no)": "connected"
}

PAIRING_FEEDBACK_COLUMNS = {
    "Timestamp": "timestamp",
    "志愿者姓名": "volunteer",
    "志愿者电子邮件": "volunteer_email",
    "志愿者家长电子邮件": "volunteer_parent_email",
    "退出志愿者姓名": "backout_volunteer",
    "退出志愿者电子邮件": "backout_volunteer_email",
    "退出志愿者家长电子邮件": "backout_volunteer_parent_email",
    "国内学生姓名": "requestee",
    "国内学生家长微信号": "requestee_wechat",
    "国内学生家长电子邮件": "requestee_email",
    "Email Address": "volunteer_email_auto"
}

VOLUNTEER_HOURS_COLUMNS = {
    "Your full name ( First and Last)": "volunteer",
    "Your email address": "email",
    "Your parent's email address": "parent_email",
    "Total volunteer hours ": "hours"
}

REGISTERED_ORGANIZATIONS_RAW = [
    "CWB",
    "Youth Hope Fund",
    "KC parenting",
    "Golden Oaks",
    "YMCCC",
    "Kansas City Institute of Chinese Language and Culture",
    "Lawrence Chinese School",
    "Carolinas Chinese American Civic Center",
    "New York Chinese Coffee Club Youth Group",
    "New Jersey Volunteer Group",
    "Asian American Civic Scholars（St. Louis)"
]
REGISTERED_ORGANIZATIONS = [org.lower() for org in REGISTERED_ORGANIZATIONS_RAW]

REQUESTEE_UNIQUE_COLS = ["parent_wechat"]
VOLUNTEER_UNIQUE_COLS = ["parent_wechat", "volunteer_email"]
PAIRING_UNIQUE_COLS = ["requestee_wechat", "volunteer_email"]


VOLUNTEER_TIME_SLOT_COLS = [
    'Available Weekday and time(Local time) [M (choose one or more)]',
    'Available Weekday and time(Local time) [T (choose one or more)]',
    'Available Weekday and time(Local time) [W (choose one or more)]',
    'Available Weekday and time(Local time) [Th (choose one or more)]',
    'Available Weekday and time(Local time) [F (choose one or more)]',
    'Available Weekend and time(Local time) [Sat (choose one or more)]',
    'Available Weekend and time(Local time) [Sun (choose one or more)]'
]

WEEKDAY_NUMBER_MAPPER = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]


DUMMY_MONDAY_DATE = '2001-01-01'  # A Monday

CHINA_UTC_OFFSET = 8

AGE_DIFF_THRESHOLD = 3
ALLOWED_HOURS_DIFF_IN_RECOMMENDATION = 2
MAX_RECOMMENDATION_NUMBER = 1
MIN_REQUESTEE_AGE = 7
MAX_MATCH_STUDENTS = 1

PRIORITY_RULES = ["doctor_family", "patient_family"]

MATCHING_CRITERIA_HARD = ["volunteer_gender", "time_slot_time"]
MATCHING_CRITERIA_SOFT = ["age"]

DATA_OUTPUT_DIR = 'data/outputs/'
PAIRING_OUTPUT_DIR = 'data/pairing_output/'
DATA_INPUT_DIR = 'data/input/'
CERTIFICATE_DIR = 'data/certificate'
OTHER_GROUP_IMG_PATH = f"{DATA_INPUT_DIR}/Org_Other_Wechat.jpeg"
INVALID_EMAIL_LIST_PATH = f"{DATA_INPUT_DIR}/invalid_email_list.csv"
INVALID_WECHAT_LIST_PATH = f"{DATA_INPUT_DIR}/invalid_wechat_list.csv"
