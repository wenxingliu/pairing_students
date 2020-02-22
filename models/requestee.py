class Requestee:
    def __init__(self, requestee_info):
        self.requestee_info = requestee_info
        self.timestamp = self.requestee_info.get('timestamp')
        self.name = self.requestee_info.get('requestee')
        self.age = self.requestee_info.get('age')
        self.gender = self.requestee_info.get('gender')
        self.parent_wechat = self.requestee_info.get('parent_wechat')
        self.doctor_family = self.requestee_info.get('doctor_family')
        self.patient_family = self.requestee_info.get('patient_family')
        self.volunteer_gender = self.requestee_info.get('volunteer_gender')
        self.scarcity_index = self.requestee_info.get('scarcity_index')
        self.time_slots_china = sorted(self.requestee_info.get('time_slots_china'))
        self._volunteer = None
        self._promised_timeslot = None

    @property
    def volunteer(self):
        return self._volunteer

    @property
    def promised_time_slot(self):
        """in china timezone"""
        return self._promised_timeslot

    @property
    def assigned(self):
        return self.volunteer is not None

    @property
    def priority(self):
        """
        Criteria: doctor family first
        Heuristic: rare requests first
        """
        return (-self.doctor_family,
                -self.patient_family,
                self.scarcity_index,
                self.timestamp)

    @property
    def time_slots_local(self):
        return f"{self.requestee_info.get('time_slot_day')}: {self.requestee_info.get('time_slot_time')}"

    def assign(self, volunteer, timeslot):
        self._volunteer = volunteer
        self._promised_timeslot = timeslot

    def __repr__(self):
        return f"{self.name} request {self.volunteer_gender}"

    def __hash__(self):
        return hash((self.name, self.parent_wechat))
