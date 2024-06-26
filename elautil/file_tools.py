import os
import configparser
import csv
from datetime import datetime

from . import config
from . import dataclasses as dc, logger

_ela_db_file_extension = ".db"
_ela_csv_file_extension = ".csv"

def extract_filename_without_extension(file_path):
    base_name = os.path.basename(file_path)  # Get the base name (filename with extension)
    filename_without_extension = os.path.splitext(base_name)[0]  # Remove the extension
    return filename_without_extension

def get_audio_data_dir_for_school_ecube(school_code):
    ecube_data_dir = os.path.join(config.ELA_DATA_DIR,'ecube')
    ecube_school_data_dir = os.path.join(ecube_data_dir,school_code)
    return ecube_school_data_dir


def find_valid_audio_data_directories(ecube_school_data_dir):
    valid_data_directories = []
    # List all directories under ecube_school_data_dir
    directories = [name for name in os.listdir(ecube_school_data_dir) if os.path.isdir(os.path.join(ecube_school_data_dir, name))]

    # Iterate over each directory to check if it's a valid data directory.abs
    # A directory is a valid data dir if 'data/log/pkg_id.txt' file exists with a [ECUBE] config section and id matches pkg_id!
    for directory in directories:
        data_dir_path = os.path.join(ecube_school_data_dir, directory)
        data_path = os.path.join(data_dir_path, 'data')
        log_path = os.path.join(data_dir_path, 'log')
        config_file = os.path.join(log_path, f"{directory}.txt")
        # Check if 'data' and 'log' directories exist
        if not os.path.isdir(data_path) or not os.path.isdir(log_path):
            continue

        # Check if config file exists
        if not os.path.isfile(config_file):
            continue

        # Parse the config file to check for 'ECUBE' section and 'id' property
        config = configparser.ConfigParser()
        config.read(config_file)

        if 'ECUBE' in config and 'id' in config['ECUBE'] and config['ECUBE']['id'] == directory:
            # If all conditions are satisfied, it's a valid data directory
            valid_data_directories.append(directory)

    return valid_data_directories

def get_audio_data_dir_for_school(school_code):
    audio_data_dir = None
    if config.ELA_AUDIO_SOURCE == 'ECUBE':
        audio_data_dir = get_audio_data_dir_for_school_ecube(school_code)
    else:
        print('UNSUPPORTED DATA SOURCE')
        exit(0)
    return audio_data_dir


def get_audio_data_files(school_code):
    logger.info(f'Scanning for audio data files for school {school_code}')
    audio_data_files = []
    if config.ELA_AUDIO_SOURCE == 'ECUBE':
        ecube_school_data_dir = get_audio_data_dir_for_school_ecube(school_code)
        package_dir_names = find_valid_audio_data_directories(ecube_school_data_dir)
        for package_dir_name in package_dir_names:
            audio_data_dir = os.path.join(ecube_school_data_dir,package_dir_name,'data')
            audio_data_file = os.path.join(audio_data_dir,package_dir_name + _ela_csv_file_extension)
            if os.path.isfile(audio_data_file):
                audio_data_files.append(audio_data_file)
            else:
                print(f'skipping corrupted package {package_dir_name} because audio data file {audio_data_file} is missing')
    else:
        print('UNSUPPORTED DATA SOURCE')
        exit(0)
    logger.info(f'Found {len(audio_data_files)} file(s)')
    return audio_data_files


def merge_school_audio_data_files(school_code,audio_data_file_list):
    combined_rows = []
    data_header = ['pkg_id','user_id','user_name','course_id','assignment_id','attempt_number','creation_time','file_name']
    # Iterate through each CSV file
    for filename in audio_data_file_list:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            pkg_id = extract_filename_without_extension(filename)
            for row in reader:
                combined_rows.append([pkg_id] + row)

    # Write combined rows to output CSV file
    merged_output_file_name = generate_csv_filename_by_timestamp(school_code)
    merged_output_file_dir = get_audio_data_dir_for_school_ecube(school_code)
    merged_file = os.path.join(merged_output_file_dir,merged_output_file_name)
    with open(merged_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_header)
        for row in combined_rows:
            writer.writerow(row)
    if os.path.isfile(merged_file):
        logger.info(f'Merged {len(audio_data_file_list)} file(s) with {len(combined_rows)} lines into {merged_file}')
        return merged_file, len(combined_rows)
    else:
        print('ERROR! Invalid merged output file')
        return None

def get_app_data_dir():
    return os.path.join(config.ELA_DATA_DIR,'ela')

def get_school_data_dir(school_code):
    data_dir = os.path.join(get_app_data_dir(),school_code)
    return data_dir

def get_school_db_file(school_code):
    db_file = os.path.join(get_school_data_dir(school_code),'ela-{}{}'.format(school_code, _ela_db_file_extension))
    return db_file

def generate_csv_filename_by_timestamp(school_code):
    return "ela-{}_{}{}".format(school_code,datetime.now().strftime("%d_%m_%Y_%H_%M_%S"),_ela_csv_file_extension)

def generate_db_filename_by_timestamp(school_code):
    return "ela-{}_{}{}".format(school_code,datetime.now().strftime("%d_%m_%Y_%H_%M_%S"),_ela_db_file_extension)

def get_new_school_db_file(school_code):
    data_dir = get_school_data_dir(school_code)
    file = generate_db_filename_by_timestamp(school_code)
    return os.path.join(data_dir,file)