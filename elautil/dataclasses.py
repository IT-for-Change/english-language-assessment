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


class TextItem:
    def __init__(self, activity_id, learner_id, package_id, asr_text, attempt_number, lang, creation_time):
        self._activity_id = activity_id
        self._learner_id = learner_id
        self._package_id = package_id
        self._attempt_number = attempt_number
        self.asr_text = asr_text
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
    
    def get_asr_text(self):
        return self._audio_file_path
    
    def get_lang(self):
        return self._lang
    
    def get_creation_time(self):
        return self._creation_time
    
    def get_text_item_id(self):
        return self._id

class ProcessedTextItem:
    def __init__(self, activity_id, learner_id, package_id, lang, creation_time):
        self._id = None
        self._activity_id = activity_id
        self._learner_id = learner_id
        self._package_id = package_id
        self._pos_counts = None
        self._total_words = None
        self._content_words = None
        self._descriptive_words = None
        self._unique_words = None
        self._long_words = None
        self._noun_phrases = None
        self._svo_triples = None
        self._sp_pairs = None
        self._lang = lang
        self._creation_time = creation_time

    # Getter methods
    def get_id(self):
        return self._id

    def get_activity_id(self):
        return self._activity_id

    def get_learner_id(self):
        return self._learner_id

    def get_package_id(self):
        return self._package_id

    def get_pos_counts(self):
        return self._pos_counts

    def get_total_words(self):
        return self._total_words

    def get_content_words(self):
        return self._content_words

    def get_descriptive_words(self):
        return self._descriptive_words

    def get_unique_words(self):
        return self._unique_words

    def get_long_words(self):
        return self._long_words

    def get_noun_phrases(self):
        return self._noun_phrases

    def get_svo_triples(self):
        return self._svo_triples

    def get_sp_pairs(self):
        return self._sp_pairs

    def get_lang(self):
        return self._lang

    def get_creation_time(self):
        return self._creation_time

    # Setter methods
    def set_id(self, id):
        self._id = id

    def set_pos_counts(self, pos_counts):
        self._pos_counts = pos_counts

    def set_total_words(self, total_words):
        self._total_words = total_words

    def set_content_words(self, content_words):
        self._content_words = content_words

    def set_descriptive_words(self, descriptive_words):
        self._descriptive_words = descriptive_words

    def set_unique_words(self, unique_words):
        self._unique_words = unique_words

    def set_long_words(self, long_words):
        self._long_words = long_words

    def set_noun_phrases(self, noun_phrases):
        self._noun_phrases = noun_phrases

    def set_svo_triples(self, svo_triples):
        self._svo_triples = svo_triples

    def set_sp_pairs(self, sp_pairs):
        self._sp_pairs = sp_pairs
