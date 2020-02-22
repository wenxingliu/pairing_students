from typing import List
from models.time_slot import TimeSlot
from models.volunteer import Volunteer
from models.requestee import Requestee
from services.utils.common import compute_time_part_from_str


class PairedInfo:
    def __init__(self, paired_info: dict):
        self.paired_info = paired_info
        self.volunteer_wechat = self.paired_info.get('volunteer_wechat')
        self.requestee_wechat = self.paired_info.get('requestee_wechat')
        self.promised_time_slot_str = self.paired_info.get('promised_time_slot')
        self.slot_start_time = self.paired_info.get('slot_start_time')
        self.slot_end_time = self.paired_info.get('slot_end_time')
        self.weekday = self.paired_info.get('weekday')
        self.volunteer_email_sent = self.paired_info.get('volunteer_email_sent')
        self.email_sent_time_utc = self.paired_info.get('email_sent_time_utc')
        self._promised_time_slot = None

    @property
    def promised_time_slot(self):
        if self._promised_time_slot is None:
            start = compute_time_part_from_str(self.slot_start_time)
            end = compute_time_part_from_str(self.slot_end_time)
            weekday_int = int(self.weekday)
            self._promised_time_slot = TimeSlot(start=start, end=end, weekday=weekday_int)
        return self._promised_time_slot

    def find_paired_requestee(self, requestee_list: List[Requestee]) -> Requestee:
        for requestee in requestee_list:
            if requestee.parent_wechat == self.requestee_wechat:
                return requestee

    def find_paired_volunteer(self, volunteer_list: List[Volunteer]) -> Volunteer:
        for volunteer in volunteer_list:
            if volunteer.parent_wechat == self.volunteer_wechat:
                return volunteer

    def __str__(self):
        return f"{self.volunteer_wechat} <-> {self.requestee_wechat}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))
