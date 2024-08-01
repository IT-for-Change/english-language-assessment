```plantuml

entity SpeechItem {
    id: (package_id, activity_id, learner_id, attempted_number)
    activity_id : string
    learner_id : string
    package_id : string
    attempt_number: int
    audio_file_path : string
    lang : string
    creation_time: string
}

entity ProcessedSpeechItem {
    id: (SpeechItem.id)
    activity_id : string
    learner_id : string
    package_id : string
    asr_text : string
    asr_text_timings : json_string
    creation_time: string 
}

entity TextItem {
    activity_id : string
    learner_id : string
    package_id : string
    asr_text : string
    attempt_number: int
    lang : string
    creation_time: string
}

entity ProcessedTextItem {
    id: string
    activity_id : string
    learner_id : string
    package_id : string
    pos_counts : json_string
    total_words: int
    content_words: int
    descriptive_words: int
    unique_words: int
    long_words: json_string
    noun_phrases: json_string
    svo_triples: json_string
    sp_pairs: json_string
    lang: string
    creation_time: string
}



```