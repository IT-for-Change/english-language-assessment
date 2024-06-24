#system
from collections import Counter
#third-party
import spacy
import pyphen
#app
from . import config
from . import logger


logger.info(f'Initializing NLP model. Loading {config.ELA_NLP_MODEL}')
_nlp = spacy.load(config.ELA_NLP_MODEL)
_dic = pyphen.Pyphen(lang='en')
logger.info('Model loaded')

def make_doc(text):
    return _nlp(text)


def sort_with_word_count(in_list, elements_have_spaces=False):
    string_counts = []
    if (elements_have_spaces):#noun phrases
        string_counts = Counter(in_list)
        string_counts = string_counts.most_common()
    else:
        in_list_text = ' '.join(map(str, in_list))
        string_counts = Counter(in_list_text.split())
        string_counts = string_counts.most_common()
    
    #print(string_counts)
    out_dict = {}
    for key, value in string_counts:
        out_dict[key] = value

    return out_dict

def extract_pos_tags(doc,include_counts=False):
   
    pos_tags = {}
    # Initialize lists for each part of speech
    nouns = []
    propnouns = []
    adjectives = []
    verbs = []
    verb_lemmas = []
    adverbs = []
    prepositions = []
    pronouns = []
    miscellaneous = []

    for sentence in doc.sents:
        # Extract nouns, adjectives, verbs, adverbs, and their lemmas
        for token in sentence:
            
            if (token.pos_ == "NOUN"):
                nouns.append(token.text.lower())
            elif (token.pos_ == 'PROPN'):
                propnouns.append(token.text.lower())
            elif token.pos_ == "ADJ":   
                adjectives.append(token.text.lower())
            elif token.pos_ == "VERB":
                verbs.append(token.text.lower())
                verb_lemmas.append(token.lemma_.lower())
            elif token.pos_ == "ADV":
                adverbs.append(token.text.lower())
            elif token.pos_ == "ADP":
                prepositions.append(token.text.lower())
            elif token.pos_ == "PRON":
                pronouns.append(token.text.lower())
            elif token.pos_ in ['PUNCT','SYM', 'NUM']:
                continue
            else:
                miscellaneous.append(token.text.lower())
    
    noun_phrases = extract_noun_phrases(doc)

    if (include_counts):
        nouns = sort_with_word_count(nouns)
        propnouns = sort_with_word_count(propnouns)
        noun_phrases = sort_with_word_count(noun_phrases,True)
        adjectives = sort_with_word_count(adjectives)
        verbs = sort_with_word_count(verbs)
        verb_lemmas = sort_with_word_count(verb_lemmas)
        adverbs = sort_with_word_count(adverbs)
        prepositions = sort_with_word_count(prepositions)
        pronouns = sort_with_word_count(pronouns)
        miscellaneous = sort_with_word_count(miscellaneous)
    

    pos_tags['NOUNS'] = nouns
    pos_tags['PROPNOUNS'] = propnouns
    pos_tags['NOUN_PHRASES'] = noun_phrases
    pos_tags['ADJECTIVES'] = adjectives
    pos_tags['VERBS'] = verbs
    pos_tags['VERBS_LEMMA'] = verb_lemmas
    pos_tags['ADVERBS'] = adverbs
    pos_tags['PREPOSITIONS'] = prepositions
    pos_tags['PRONOUNS'] = pronouns
    pos_tags['MISC'] = miscellaneous

    return pos_tags

def extract_noun_phrases(doc):
    
    noun_phrases = []
    for chunk in doc.noun_chunks:
        words_in_chunk = chunk.text.split(' ')
        words_in_chunk_count = len(words_in_chunk)
        if (words_in_chunk_count > 1):
            if (words_in_chunk_count == 2):
                if (words_in_chunk[0] not in ['a','an','the']):
                    noun_phrases.append(chunk.text.lower())
            else:
                noun_phrases.append(chunk.text.lower())

    return noun_phrases

def nan_to_empty_string(value):
    if pd.isna(value):
        return ''
    else:
        return str(value)

def estimate_of_syllables(word):
    syllables = len(dic.inserted(word).split('-'))
    if (len(word) > 4 and syllables == 1): #correct the estimate for issues in pyphen library for short 2-syllable words.
        syllables = 2
    return syllables

'''==== BEGIN: NLP TREE PARSER BASED FUNCTIONS ===='''

def traverse_dependency_tree(token, depth=0):
    print("  " * depth + f"{token.text} ({token.dep_}|{token.pos_}|{token.tag_})")
    for child in token.children:
        traverse_dependency_tree(child, depth + 1)

def is_root_token(token):
    if (token.dep_ == 'ROOT'):
        if token.pos_ in ['VERB', 'AUX']:
            return True


def get_predicate_verb(sentence):
    verb_aux = None
    verb = None
    for token in sentence:
        if (token.dep_ == 'ROOT'):
            if token.pos_ == 'VERB':
                verb = token.text
            elif token.pos_ == 'AUX':
                verb_aux = token.text
            else:
                continue
    return verb, verb_aux

def get_predicate_verb_v2(sentence):
    is_verb_aux = False
    verb = None
    for token in sentence:
        if (token.dep_ == 'ROOT'):
            if token.pos_ == 'VERB':
                verb = token.text
            elif token.pos_ == 'AUX':
                verb = token.text
                is_verb_aux = True
            else:
                continue
    return verb, is_verb_aux

def get_adjectives(sentence):
    adjectives = []
    for token in sentence:
            if token.pos_ == 'ADJ':
                adjectives.append(token.text)
            else:
                continue
    return adjectives

def get_adverbs(sentence):
    adverbs = []
    for token in sentence:
            if token.pos_ == 'ADV':
                adverbs.append(token.text)
            else:
                continue
    return adverbs

def get_pronouns(sentence):
    pronouns = []
    for token in sentence:
            if token.pos_ == 'PRON':
                pronouns.append(token.text)
            else:
                continue
    return pronouns

def get_prepositions(sentence):
    prepositions = []
    for token in sentence:
            if token.pos_ == 'ADP':
                prepositions.append(token.text)
            else:
                continue
    return prepositions

def get_all_verbs(sentence):
    verbs = []
    for token in sentence:
            if token.pos_ == 'VERB':
                verbs.append(token.text)
            else:
                continue
    return verbs

def get_noun_subjects(sentence):
    noun_subjects = []
    for token in sentence:
        if (token.dep_ in ["nsubj", "nsubjpass"]):
            noun_subjects.append(token.text)            
    return noun_subjects

def get_noun_objects(sentence):
    noun_objects = []
    for token in sentence:
        if (token.dep_ in ["dobj", "pobj", "dative"]):
            noun_objects.append(token.text)
    return noun_objects

def get_fragment_from_sentence(sentence, in_token, token_last_matched_index):
    fragment = ''
    token_index = 0
    for i, token in enumerate(sentence):
        if token.text == in_token.text:
            if (i == token_last_matched_index): 
                #this repeats in the sentence, and has been matched in a prev iteration, 
                # so ignore it and continue looking for the next occurrence of the token in the sentence
                continue
            token_index = i
            break

    tokens = [token.text for token in sentence]
    if len(tokens) == 0:
        fragment = ''
    else:
        start_index = max(0, token_index - 3)
        end_index = min(len(tokens), token_index + 3)
        fragment = ' '.join(tokens[start_index:end_index])

    return fragment, token_index

def get_clause_fragments(sentence):
    clause_fragments = []
    clause_marker_found = False
    token_last_matched_index = 0
    for token in sentence:
        if (token.dep_ in ["mark"] and clause_marker_found == False):
            clause_marker_found = True
            clause_fragment, token_last_matched_index = get_fragment_from_sentence(sentence,token,token_last_matched_index)
        elif (token.dep_ in ["advcl", "relcl", "csubj"] and clause_marker_found == False):
            clause_marker_found = True
            clause_fragment, token_last_matched_index = get_fragment_from_sentence(sentence,token,token_last_matched_index)
        else:
            continue
        clause_fragments.append(clause_fragment)
    return clause_fragments

def get_coord_conjunctions(sentence):
    cconj_fragments = []
    token_last_matched_index = 0
    for token in sentence:
        if (token.dep_ in ["cc"]):
            cconj_fragment, token_last_matched_index = get_fragment_from_sentence(sentence,token, token_last_matched_index)
            cconj_fragments.append(cconj_fragment)
    return cconj_fragments

def print_dependency_tree(sentence):
    for token in sentence:
        if (is_root_token(token)):
            traverse_dependency_tree(token)

def print_dependency_tree(sentences):
    for sentence in sentences:
        for token in sentence:
            if (is_root_token(token)):
                traverse_dependency_tree(token)

def predicate_verbs(doc,aux_verbs=False):
    predicate_verbs = []
    predicate_verbs_aux = []
    sentences = list(doc.sents)
    for sentence in sentences:
        predicate_verb, predicate_verb_aux = get_predicate_verb(sentence)
        if (predicate_verb != None):
            predicate_verbs.append(predicate_verb)
        if (predicate_verb_aux != None and aux_verbs == True):
            predicate_verbs_aux.append(predicate_verb_aux)
    
    return predicate_verbs, predicate_verbs_aux

def noun_subjects(doc):
    noun_subjects_all = []
    sentences = list(doc.sents)
    for sentence in sentences:
        noun_subjects = get_noun_subjects(sentence)
        noun_subjects_all.extend(noun_subjects)
    return noun_subjects_all

def noun_objects(doc):
    noun_objects_all = []
    sentences = list(doc.sents)
    for sentence in sentences:
        noun_objects = get_noun_objects(sentence)
        noun_objects_all.extend(noun_objects)
    return noun_objects_all

def noun_phrases(doc):
    noun_phrases = extract_noun_phrases(doc)
    return noun_phrases

def clauses_as_fragments(doc):
    clause_fragments_all = []
    sentences = list(doc.sents)
    for sentence in sentences:
        clause_fragments = get_clause_fragments(sentence)
        clause_fragments_all.extend(clause_fragments)
    return clause_fragments_all

def coord_conjugations(doc):
    cconj_fragments_all = []
    sentences = list(doc.sents)
    for sentence in sentences:
        cconj_fragments = get_coord_conjunctions(sentence)
        cconj_fragments_all.extend(cconj_fragments)
    return cconj_fragments_all


'''==== END: NLP TREE PARSER BASED FUNCTIONS ===='''

def analyze_sentences(doc):
    sentences = doc.sents
    sentence_analysis = []
    sentence_id = 0
    for sentence in sentences:
        sentence_id += 1
        len_sentence = len(sentence)
        predicate_verb, is_predicate_verb_aux = get_predicate_verb_v2(sentence)
        verbs = get_all_verbs(sentence)
        count_of_verbs = len(verbs)
        noun_subjects = get_noun_subjects(sentence)
        count_of_noun_subjects = len(noun_subjects)
        noun_objects = get_noun_objects(sentence)
        count_of_noun_objects = len(noun_objects)
        adjectives = get_adjectives(sentence)
        count_of_adjectives = len(adjectives)
        adverbs = get_adverbs(sentence)
        count_of_adverbs = len(adverbs)
        pronouns = get_pronouns(sentence)
        count_of_pronouns = len(pronouns)
        prepositions = get_prepositions(sentence)
        count_of_prepositions = len(prepositions)
        clause_fragments = get_clause_fragments(sentence)
        count_of_clause_fragments = len(clause_fragments)
        sentence_analysis.append(
            (sentence_id,
            len_sentence,
            predicate_verb,
            is_predicate_verb_aux,
            verbs,
            count_of_verbs,
            count_of_noun_subjects,
            noun_subjects,
            count_of_noun_objects,
            noun_objects,
            count_of_adjectives,
            adjectives,
            count_of_adverbs,
            adverbs,
            count_of_pronouns,
            pronouns,
            count_of_prepositions,
            prepositions,
            count_of_clause_fragments,
            clause_fragments)
        )
    
    return sentence_analysis