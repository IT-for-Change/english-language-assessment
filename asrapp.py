import csv

from elautil import file_tools, logger, asrutil, eladb

school_code = '1020' #--school_code 1020
generate_new_db = False # --generate-new-db
export_to_csv = True # --export_csv
audio_data_files = file_tools.get_audio_data_files(school_code)
merged_filename, lines_in_file = file_tools.merge_school_audio_data_files(school_code,audio_data_files)
speech_items = asrutil.get_speech_items(school_code,merged_filename)

asrutil.process_speech_items(school_code,speech_items, generate_new_db,export_to_csv)


