import os

#defaults for local testing
os.environ['ELA_DATA_DIR'] = 'files/data'
os.environ['ELA_LOG_DIR'] = 'files/log'
os.environ['ELA_ASR_MODEL'] = 'files/models/whisper/small.en.pt'
os.environ['ELA_ASR_INFERENCE_DEVICE'] = 'cpu'
os.environ['ELA_NLP_MODEL'] = 'en_core_web_trf'
os.environ['ECUBE_PKG_AUDIO_DIR'] = 'data/audio'
os.environ['ELA_SERVER_TIMEZONE'] = 'Asia/Kolkata'
os.environ['ELA_AUDIO_SOURCE'] = 'ECUBE' #'ECUBE' #OTHER POSSIBLE VALUE(S): 'BYRA'


#mandatory variables
ELA_DATA_DIR = os.environ['ELA_DATA_DIR']
ELA_LOG_DIR = os.environ['ELA_LOG_DIR']
ELA_ASR_MODEL = os.environ['ELA_ASR_MODEL']
ELA_ASR_INFERENCE_DEVICE = os.environ['ELA_ASR_INFERENCE_DEVICE'] 
ELA_NLP_MODEL = os.environ['ELA_NLP_MODEL']
ECUBE_PKG_AUDIO_DIR = os.environ['ECUBE_PKG_AUDIO_DIR']
ELA_SERVER_TIMEZONE = os.environ['ELA_SERVER_TIMEZONE']
ELA_AUDIO_SOURCE = os.environ['ELA_AUDIO_SOURCE']


#optional
ELA_LOG_LEVEL = os.environ.get('ELA_LOG_LEVEL', 'INFO')


#constants
ELA_LOG_FILE = 'ela.log'
ELA_ASSESSMENTAUDIT_LOCALDB_NAME = 'ela-audit.db'
#fileops
ECUBE_PKG_CSV_DIR = 'data'
ECUBE_PKG_AUDIO_DIR = 'data/audio'
ECUBE_PKG_LOG_DIR = 'log'

BYRA_PKG_AUDIO_DIR = 'media'

