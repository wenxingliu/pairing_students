class Requestee:
    def __init__(self, requestee_info):
        self.requestee_info = requestee_info
        self.timestamp = self.requestee_info.get('timestamp')
        self.name = self.requestee_info.get('requestee')
        self.age = self.requestee_info.get('age')
        self.gender = self.requestee_info.get('gender')
        self.parent_wechat = self.requestee_info.get('parent_wechat')
        self.other_wechat_info = self.requestee_info.get('other_wechat_info')
        self.doctor_family = self.requestee_info.get('doctor_family', 0)
        self.patient_family = self.requestee_info.get('patient_family', 0)
        self.volunteer_gender = self.requestee_info.get('volunteer_gender')
        self.scarcity_index = self.requestee_info.get('scarcity_index', 0)
        self.time_slots_china = sorted(self.requestee_info.get('time_slots_china'))
        self._volunteer = None
        self._promised_time_slot = None
        self.recommendation_made = False

    @property
    def volunteer(self):
        return self._volunteer

    @property
    def promised_time_slot(self):
        """in china timezone"""
        return self._promised_time_slot

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
        self._promised_time_slot = timeslot

    @property
    def formatted_info(self) -> str:
        if self.assigned:
            time_str = f"Tentative Time (Beijing Time): {self.promised_time_slot}"
        else:
            time_str = f"Preferred Time (Beijing Time): {self.time_slots_local}"

        formatted_text = f"""
        Name: {self.name.title()}
        {time_str} 
        Age: {self.requestee_info.get('age_raw')}
        Gender: {self.gender.title()}
        Parent Wechat: {self.parent_wechat}
        English Learning (Years): {self.requestee_info.get('english_learning_in_years')}
        Preferred Content: {self.requestee_info.get('content')}
        Doctor Family: {"Yes" if self.doctor_family else "No"}
        COVID-19 Patient Family: {"Yes" if self.patient_family else "No"}\n
        """

        if self.other_wechat_info:
            formatted_text += f"""
            Our data suggests there are more than one wechat accounts on file:
            {self.other_wechat_info}
            """

        return formatted_text

    def __str__(self):
        return f"{self.name} request {self.volunteer_gender}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.name, self.parent_wechat))
