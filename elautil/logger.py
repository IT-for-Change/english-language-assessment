import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
import os
import sys
import pytz
from pathlib import Path
from datetime import datetime, timezone

#app
from .config import ELA_SERVER_TIMEZONE, ELA_LOG_DIR, ELA_LOG_FILE, ELA_LOG_LEVEL

class ELATimezoneFormatter(Formatter):

    def formatTime(self, record, datefmt=None):
        dt_utc = datetime.fromtimestamp(record.created, tz=timezone.utc)
        server_tz = pytz.timezone(ELA_SERVER_TIMEZONE)
        dt_server = dt_utc.astimezone(server_tz)
        return dt_server.strftime(datefmt)


print(f'Initializing logging: {ELA_LOG_FILE}')
file_size_bytes = 500 * 1024  # Set the maximum file size (in bytes) before rotation
backup_count = 10  # Set the number of backup files to keep
    
logDir = ELA_LOG_DIR
logfile = os.path.join(ELA_LOG_DIR, ELA_LOG_FILE)
if (os.path.exists(logDir) == False):
    Path(logDir).mkdir(parents=True)

rotating_file_handler = RotatingFileHandler(logfile,maxBytes=file_size_bytes,backupCount=backup_count)
formatter = ELATimezoneFormatter('%(asctime)s - %(levelname)s: %(message)s',\
        datefmt = '%d/%m/%Y %I:%M:%S %p')
rotating_file_handler.setFormatter(formatter)

logging.basicConfig(handlers=[rotating_file_handler])
logging.getLogger().setLevel(logging.getLevelName(ELA_LOG_LEVEL))

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO) #log info and above to console. debug goes only to file
formatter = ELATimezoneFormatter('%(asctime)s - %(levelname)s: %(message)s',\
                     datefmt = '%d/%m/%Y %I:%M:%S %p' )
stream_handler.setFormatter(formatter)
logging.getLogger().addHandler(stream_handler)

#watchdog module adds debug log that floods the log file. so set it to INFO
logging.getLogger('watchdog.observers.inotify').setLevel(logging.INFO)
logging.getLogger('watchdog.observers.inotify_buffer').setLevel(logging.INFO)

logging.info(f'Logging initialized: {logfile}')

def log_info(message):
    logging.info(message)

def log_debug(message):
    logging.debug(message)

def log_error(message):
    logging.error(message)
