import datetime as dt
from typing import List

import settings as settings


class TimeSlot:
    def __init__(self, start: dt.datetime,
                 end: dt.datetime,
                 weekday: int = None,
                 scarcity_index: int = None):
        self.start = start.time()
        self.end = end.time()
        self.weekday = weekday
        self.weekday_name = settings.WEEKDAY_NUMBER_MAPPER[self.weekday]
        self.scarcity_index = scarcity_index
        self._fake_start_datetime = None
        self._fake_end_datetime = None

    @property
    def fake_start_datetime(self):
        if self._fake_start_datetime is None:
            self._fake_start_datetime = self.fake_datetime(self.start, self.weekday)
        return self._fake_start_datetime

    @property
    def fake_end_datetime(self):
        if self._fake_end_datetime is None:
            self._fake_end_datetime = self.fake_datetime(self.end, self.weekday)
        return self._fake_end_datetime

    @property
    def name(self) -> str:
        return f"{self.weekday_name} {self.start.strftime('%H:%M')}-{self.end.strftime('%H:%M')}"

    @staticmethod
    def fake_datetime(time_obj, weekday):
        dt_str = f"{settings.DUMMY_MONDAY_DATE} {time_obj}"
        dt_obj = dt.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S") + dt.timedelta(days=weekday)
        return dt_obj

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __gt__(self, other):
        return (self.weekday, self.start.hour, self.start.minute) >= (other.weekday, other.end.hour, other.end.minute)

    def __lt__(self, other):
        return (self.weekday, self.end.hour, self.end.minute) <= (other.weekday, other.start.hour, other.end.minute)


class TimeSlotList:
    def __init__(self, time_slot_list: List[TimeSlot]):
        self.list = sorted(time_slot_list)

    @property
    def len(self):
        return len(self.list)

    def pop(self, i):
        return self.list.pop(i)

    def __getitem__(self, i):
        return self.list[i]

    def __eq__(self, other):
        return self.list == other.list

    def __repr__(self):
        return str(self.list)


def local_time_slot_to_utc(time_slots_local, utc_offset):
    utc_time_slots = []
    for time_slot in time_slots_local:
        utc_start = time_slot.fake_start_datetime - dt.timedelta(hours=utc_offset)
        utc_end = time_slot.fake_end_datetime - dt.timedelta(hours=utc_offset)
        utc_weekday = utc_start.weekday()
        utc_time_slot = TimeSlot(start=utc_start,
                                 end=utc_end,
                                 weekday=utc_weekday,
                                 scarcity_index=time_slot.scarcity_index)
        utc_time_slots.append(utc_time_slot)
    return TimeSlotList(utc_time_slots)


def utc_time_slot_to_china_tz(time_slots_utc):
    china_time_slots = []
    for time_slot in time_slots_utc:
        china_start = time_slot.fake_start_datetime + dt.timedelta(hours=settings.CHINA_UTC_OFFSET)
        china_end = time_slot.fake_end_datetime + dt.timedelta(hours=settings.CHINA_UTC_OFFSET)
        china_weekday = china_start.weekday()
        china_time_slot = TimeSlot(start=china_start,
                                   end=china_end,
                                   weekday=china_weekday,
                                   scarcity_index=time_slot.scarcity_index)
        china_time_slots.append(china_time_slot)
    return TimeSlotList(china_time_slots)
