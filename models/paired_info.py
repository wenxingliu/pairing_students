from models.time_slot import TimeSlot
from services.utils.common import compute_time_part_from_str


class PairedInfo:
    def __init__(self, paired_info: dict):
        self.paired_info = paired_info
        self.volunteer_wechat = self.paired_info.get('volunteer_wechat')
        self.requestee_wechat = self.paired_info.get('requestee_wechat')
        self.volunteer_name = self.paired_info.get('volunteer')
        self.volunteer_email = self.paired_info.get('volunteer_email')
        self.volunteer_parent_email = self.paired_info.get('volunteer_parent_email')
        self.requestee_name = self.paired_info.get('requestee')
        self.promised_time_slot_str = self.paired_info.get('promised_time_slot')
        self.slot_start_time = self.paired_info.get('slot_start_time')
        self.slot_end_time = self.paired_info.get('slot_end_time')
        self.weekday = self.paired_info.get('weekday')
        self.volunteer_email_sent = self.paired_info.get('volunteer_email_sent')
        self.email_sent_time_utc = self.paired_info.get('timestamp')
        self._promised_time_slot = None
        self.valid = True

    @property
    def promised_time_slot(self):
        if self._promised_time_slot is None:
            start = compute_time_part_from_str(self.slot_start_time)
            end = compute_time_part_from_str(self.slot_end_time)
            weekday_int = int(self.weekday)
            self._promised_time_slot = TimeSlot(start=start, end=end, weekday=weekday_int)
        return self._promised_time_slot

    def __str__(self):
        return f"{self.volunteer_name} ({self.volunteer_wechat}) -> {self.requestee_name} ({self.requestee_wechat})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))
