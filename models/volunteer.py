import datetime as dt
from typing import List
from models.time_slot import TimeSlot, local_time_slot_to_utc, utc_time_slot_to_china_tz

import settings

class Volunteer:
    def __init__(self, volunteer_info: dict):
        self.volunteer_info = volunteer_info
        self.name = self.volunteer_info.get('name')
        self.volunteer_email = self.volunteer_info.get('volunteer_email')
        self.parent_wechat = self.volunteer_info.get('parent_wechat')
        self.parent_email = self.volunteer_info.get('parent_email')
        self.time_slots_local = sorted(self.volunteer_info.get('time_slots_local'))
        self.utc_offset = self.volunteer_info.get('utc_offset')
        self.gender = self.volunteer_info.get('volunteer_gender')
        self.age = self.volunteer_info.get('age')
        self.num_pairs = self.volunteer_info.get('num_pairs', 1)
        self.timezone = self.volunteer_info.get('timezone')
        self.organization = self.volunteer_info.get('organization')
        self.scarcity_index = self.volunteer_info.get('scarcity_index')
        self._time_slots_utc = None
        self._time_slots_china = None
        self._paired_student = []
        self._potential_match = []
        self._email_sent_time_utc = None

    @property
    def no_org(self) -> bool:
        return str(self.organization) not in settings.REGISTERED_ORGANIZATIONS

    @property
    def paired_student(self):
        return self._paired_student

    @property
    def recommendation_made(self):
        return self.available and (len(self.potential_match) > 0)

    @property
    def potential_match(self):
        return self._potential_match

    @property
    def available_spots(self):
        return self.num_pairs - len(self.paired_student)

    @property
    def available(self) -> bool:
        return (self.available_spots > 0) and (self.time_slots_china.len > 0)

    @property
    def time_slots_utc(self) -> List[TimeSlot]:
        if self._time_slots_utc is None:
            self._time_slots_utc = local_time_slot_to_utc(self.time_slots_local,
                                                          self.utc_offset)
        return self._time_slots_utc

    @property
    def time_slots_china(self) -> List[TimeSlot]:
        if self._time_slots_china is None:
            self._time_slots_china = utc_time_slot_to_china_tz(self.time_slots_utc)
        return self._time_slots_china

    @property
    def email_sent_time_utc(self) -> bool:
        return self._email_sent_time_utc

    @property
    def email_sent(self) -> bool:
        return self.email_sent_time_utc is not None

    def overlapping_china_time_slots(self, time_slots_china: List[TimeSlot]) -> List[TimeSlot]:
        overlaps = list(set(time_slots_china).intersection(self.time_slots_china))
        return overlaps

    def assign(self, student, promised_time_slot):
        """promised_time_slot in china timezone"""
        self._paired_student.append(student)
        self._remove_china_time_slot(promised_time_slot)

    def recommend(self, student):
        self._potential_match.append(student)

    def mark_email_sent(self, sent_time=None):
        sent_time = sent_time or dt.datetime.utcnow()
        self._email_sent_time_utc = sent_time

    def _remove_china_time_slot(self, time_slot: TimeSlot):
        for i, volunteer_time_slot in enumerate(self.time_slots_china):
            if volunteer_time_slot == time_slot:
                break
        self.time_slots_china.pop(i)

    def __str__(self):
        return f"{self.name} {self.timezone} (Age {self.age}; Gender: {self.gender})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.parent_wechat)
