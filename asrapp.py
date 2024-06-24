import csv
from elautil import file_tools, logger

school_code = '1020'
logger.info(f'Scanning for audio data files for school {school_code}')
audio_data_files = file_tools.get_audio_data_files(school_code)
logger.info(f'Found {len(audio_data_files)} file(s)')
merged_filename, lines_in_file = file_tools.merge_school_audio_data_files(school_code,audio_data_files)
logger.info(f'Merged {len(audio_data_files)} file(s) with {lines_in_file} lines into {merged_filename}')
print(merged_filename)
