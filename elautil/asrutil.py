import os
import csv
import whisper_timestamped as whisper
from . import file_tools, config, dataclasses as dc, logger, eladb

logger.info(f'Initializing ASR model. Loading {config.ELA_ASR_MODEL}')
model = whisper.load_model(config.ELA_ASR_MODEL, device=config.ELA_ASR_INFERENCE_DEVICE)
logger.info('Model initialized')

def create_new_speech_item(school_code,data_source_format,row):
    speech_item = None
    if data_source_format == 'ECUBE':
        speech_item = create_new_speech_item_ecube(school_code,row)
    if data_source_format == 'BYRA':
        speech_item = create_new_speech_item_byra(school_code,row)
    return speech_item

def create_new_speech_item_ecube(school_code,row):
    pkg_id = row['pkg_id']
    user_name = row['user_name']
    user_id = row['user_id']
    course_id = row['course_id']
    activity_id = row['assignment_id']
    attempt_number = row['attempt_number']
    creation_time = row['creation_time']
    audio_file_name = row['file_name']
    lang = 'en'
    #print("{},{},{},{}".format(file_tools.get_audio_data_dir_for_school(school_code),pkg_id,config.ECUBE_PKG_AUDIO_DIR,audio_file_name))
    audio_full_file_name = os.path.join(file_tools.get_audio_data_dir_for_school_ecube(school_code),pkg_id,config.ECUBE_PKG_AUDIO_DIR,audio_file_name)
    speech_item = dc.SpeechItem(
        activity_id,
        user_name, 
        pkg_id, 
        attempt_number,
        audio_full_file_name, 
        lang,
        creation_time
    )
    return speech_item

def create_new_speech_item_byra(school_code,row):
    pkg_id = row['pkg_id']
    user_name = row['asr_collect_data-studentid']
    user_id = row['asr_collect_data-studentid']
    course_id = row['pkg_id']
    activity_id = row['pkg_id']
    attempt_number = 1
    creation_time = row['startTime']
    audio_file_name = row['asr_collect_data-student_recording']
    lang = 'en'
    #print("{},{},{},{}".format(file_tools.get_audio_data_dir_for_school(school_code),pkg_id,config.ECUBE_PKG_AUDIO_DIR,audio_file_name))
    audio_full_file_name = os.path.join(file_tools.get_audio_data_dir_for_school_byra(school_code),pkg_id,config.BYRA_PKG_AUDIO_DIR,audio_file_name)
    speech_item = dc.SpeechItem(
        activity_id,
        user_name, 
        pkg_id, 
        attempt_number,
        audio_full_file_name, 
        lang,
        creation_time
    )
    return speech_item

def get_speech_items(school_code,data_source_format,merged_school_audio_data_file):
    speech_items = []
    with open(merged_school_audio_data_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            speech_item = create_new_speech_item(school_code,data_source_format,row)
            speech_items.append(speech_item)

    return speech_items

def asr_process(audio_file):
    asr_text = 'mic testing'
    asr_text_timings = '\{\}'
    result = whisper.transcribe(model, audio_file, beam_size=5, best_of=5, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),detect_disfluencies=True, vad=True)
    asr_text = result["text"]
    asr_text = asr_text.lower().strip()
    logger.debug(f'Transcribed text: {asr_text}')
    all_words = []
    segments = result["segments"]
    for segment in segments:
        all_words.extend(segment["words"])

    asr_text_timings = str(all_words)
    return asr_text, asr_text_timings

def process_single_speech_item(speech_item):
    audio_file = speech_item.get_audio_file_path()
    logger.info("{}|{}".format(speech_item.get_speech_item_id(),"Performing ASR"))
    asr_text, asr_text_timings = asr_process(audio_file)
    logger.info("{}|{}".format(speech_item.get_speech_item_id(),"ASR completed"))
    processed_speech_item = dc.ProcessedSpeechItem(
        speech_item.get_speech_item_id(),
        speech_item.get_activity_id(),
        speech_item.get_learner_id(),
        speech_item.get_package_id(),
        asr_text,
        asr_text_timings,
        speech_item.get_creation_time()
    )
    return processed_speech_item

def process_speech_items(school_code,speech_items,generate_new_db=False,export_to_csv=False):
    db_file = ''
    if (generate_new_db):
        db_file = file_tools.get_new_school_db_file(school_code)
    else:
        db_file = file_tools.get_school_db_file(school_code)
    db = eladb.ELADB(db_file)
    for speech_item in speech_items:
        item_exists_in_db = False
        if (generate_new_db):
            item_exists_in_db = False
        else:
            item_exists_in_db = db.check_speech_item_exists(speech_item.get_speech_item_id())
        if (item_exists_in_db == False):
            processed_speech_item = process_single_speech_item(speech_item)
            db.insert_processed_speech_item(processed_speech_item)
    
    if (export_to_csv):
        csv_file = file_tools.generate_csv_filename_by_timestamp(school_code)
        csv_dir = file_tools.get_school_data_dir(school_code)
        logger.info('Exporting to {}/{}'.format(csv_dir,csv_file))
        db.export_asr_csv(csv_dir,csv_file)
        logger.info('Export complete')
    return