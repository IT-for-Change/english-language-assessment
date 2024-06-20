#system
from collections import Counter
#third-party
import spacy
import pyphen
#app
from .config import ELA_NLP_MODEL
from .logger import log_info, log_error, log_debug


log_info(f'Initializing NLP model. Loading {ELA_NLP_MODEL}')
nlp = spacy.load(ELA_NLP_MODEL)
dic = pyphen.Pyphen(lang='en')
log_info('Model loaded')
