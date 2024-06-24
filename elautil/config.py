import os

#defaults for local testing
os.environ['ELA_DATA_DIR'] = 'files/data'
os.environ['ELA_LOG_DIR'] = 'files/log'
os.environ['ELA_TRIGGER_DIR'] = '.'
os.environ['ELA_TRIGGER_FILE'] = '.trigger'
os.environ['ELA_ASR_MODEL'] = 'medium.en'
os.environ['ELA_ASR_INFERENCE_DEVICE'] = 'cpu'
os.environ['ELA_NLP_MODEL'] = 'en_core_web_trf'
os.environ['PKG_UPLOAD_BASE_DIR'] = '=files/data/ecube'
os.environ['ELA_LOCALDB_DIR'] = 'files/data/ela'
os.environ['ELA_SERVER_TIMEZONE'] = 'Asia/Kolkata'
os.environ['ELA_AUDIO_SOURCE'] = 'ECUBE' #CAN BE ODK ALSO


#mandatory variables
ELA_DATA_DIR = os.environ['ELA_DATA_DIR']
ELA_LOG_DIR = os.environ['ELA_LOG_DIR']
ELA_TRIGGER_DIR = os.environ['ELA_TRIGGER_DIR']
ELA_TRIGGER_FILE = os.environ['ELA_TRIGGER_FILE']
ELA_ASR_MODEL = os.environ['ELA_ASR_MODEL']
ELA_ASR_INFERENCE_DEVICE = os.environ['ELA_ASR_INFERENCE_DEVICE'] 
ELA_NLP_MODEL = os.environ['ELA_NLP_MODEL']
PKG_UPLOAD_BASE_DIR = os.environ['PKG_UPLOAD_BASE_DIR']
ELA_LOCALDB_DIR = os.environ['ELA_LOCALDB_DIR']
ELA_SERVER_TIMEZONE = os.environ['ELA_SERVER_TIMEZONE']
ELA_AUDIO_SOURCE = os.environ['ELA_AUDIO_SOURCE']


#optional
ELA_LOG_LEVEL = os.environ.get('ELA_LOG_LEVEL', 'INFO')


#constants
ELA_LOG_FILE = 'ela.log'
ELA_ASSESSMENTAUDIT_LOCALDB_NAME = 'ela-audit.db'
#fileops
PKG_CSV_REL_DIR = 'data'
PKG_AUDIO_REL_DIR = 'data/audio'
PKG_META_LOG_DIR = 'log'

