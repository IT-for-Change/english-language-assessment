class SpeechItem:
    def __init__(self, activity_id, learner_id, package_id, attempt_number, audio_file_path, lang, creation_time):
        self._activity_id = activity_id
        self._learner_id = learner_id
        self._package_id = package_id
        self._attempt_number = attempt_number
        self._audio_file_path = audio_file_path
        self._lang = lang
        self._creation_time = creation_time
        self._id = "{}-{}-{}-{}".format(package_id,activity_id,learner_id,attempt_number)
    
    def get_activity_id(self):
        return self._activity_id
    
    def get_learner_id(self):
        return self._learner_id
    
    def get_package_id(self):
        return self._package_id
    
    def get_attempt_number(self):
        return self._attempt_number
    
    def get_audio_file_path(self):
        return self._audio_file_path
    
    def get_lang(self):
        return self._lang
    
    def get_creation_time(self):
        return self._creation_time
    
    def get_speech_item_id(self):
        return self._id


class ProcessedSpeechItem:
    def __init__(self, id, activity_id, learner_id, package_id, asr_text, asr_text_timings, creation_time):
        self._id = id
        self._activity_id = activity_id
        self._learner_id = learner_id
        self._package_id = package_id
        self._asr_text = asr_text
        self._asr_text_timings = asr_text_timings
        self._creation_time = creation_time
    
    def get_id(self):
        return self._id
    
    def get_activity_id(self):
        return self._activity_id
    
    def get_learner_id(self):
        return self._learner_id
    
    def get_package_id(self):
        return self._package_id
    
    def get_asr_text(self):
        return self._asr_text
    
    def get_asr_text_timings(self):
        return self._asr_text_timings
    
    def get_creation_time(self):
        return self._creation_time
