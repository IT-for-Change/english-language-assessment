# eladb.py

import sqlite3
import os
import csv
from contextlib import closing
from . import logger

class ELADB:
    def __init__(self, filename):
        self.db_file = filename
        self.connection = None
        self._initialize_database()

    def _initialize_database(self):
        # Create directory if it doesn't exist
        if not os.path.exists(os.path.dirname(self.db_file)):
            os.makedirs(os.path.dirname(self.db_file))
        
        # Connect to the database
        self.connection = sqlite3.connect(self.db_file)
        
        with closing(self.connection.cursor()) as cursor:
            # Create table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS processed_speech_item_t (
                    id TEXT PRIMARY KEY,
                    activity_id TEXT NOT NULL,
                    learner_id TEXT NOT NULL,
                    package_id TEXT NOT NULL,
                    asr_text TEXT NOT NULL,
                    asr_text_timings TEXT NOT NULL,
                    creation_time TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS processed_text_item_t (
                    id TEXT PRIMARY KEY,
                    activity_id TEXT NOT NULL,
                    learner_id TEXT NOT NULL,
                    package_id TEXT NOT NULL,
                    asr_text TEXT NOT NULL,
                    asr_text_timings TEXT NOT NULL,
                    creation_time TEXT NOT NULL
                )
            ''')

            self.connection.commit()

    def check_speech_item_exists(self, speech_item_id):
        try:
            with closing(self.connection.cursor()) as cursor:
            # Check if the id already exists
                cursor.execute('SELECT id FROM processed_speech_item_t WHERE id = ?', (speech_item_id,))
                if cursor.fetchone() is not None:
                    logger.info(f"id {speech_item_id} already exists. Skipping")
                    return True
                else:
                    return False
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return False
            

    def insert_processed_speech_item(self, item):
        try:
            with closing(self.connection.cursor()) as cursor:
                # Check if the id already exists
                cursor.execute('SELECT id FROM processed_speech_item_t WHERE id = ?', (item.get_id(),))
                if cursor.fetchone() is not None:
                    logger.info(f"id {item.get_id()} already exists. Skipping")
                    return
                
                # Insert the new record
                cursor.execute('''
                    INSERT INTO processed_speech_item_t (id, activity_id, learner_id, package_id, asr_text, asr_text_timings, creation_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (item.get_id(), 
                    item.get_activity_id(), 
                    item.get_learner_id(), 
                    item.get_package_id(), 
                    item.get_asr_text(), 
                    item.get_asr_text_timings(), 
                    item.get_creation_time())
                    )
                self.connection.commit()
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")

    def export_asr_csv(self, file_directory, filename):
        csv_path = os.path.join(file_directory, filename)
        try:
            with closing(self.connection.cursor()) as cursor:
                cursor.execute('SELECT * FROM processed_speech_item_t')
                rows = cursor.fetchall()
                headers = [description[0] for description in cursor.description]
                
                # Write to CSV
                with open(csv_path, 'w', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(headers)
                    csvwriter.writerows(rows)
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")

   
    def check_processed_text_item_exists(self, text_item_id):
        try:
            with closing(self.connection.cursor()) as cursor:
            # Check if the id already exists
                cursor.execute('SELECT id FROM processed_text_item_t WHERE id = ?', (text_item_id,))
                if cursor.fetchone() is not None:
                    logger.info(f"id {text_item_id} already exists. Skipping")
                    return True
                else:
                    return False
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return False
   
    def add_processed_text_item(connection, item):
        if check_processed_text_item_exists(connection, item.get_id()):
            print("id already exists")
            return
        try:
            with closing(connection.cursor()) as cursor:
                cursor.execute('''
                    INSERT INTO processed_text_item_t (id, activity_id, learner_id, package_id, pos_counts, total_words, content_words, descriptive_words, unique_words, long_words, noun_phrases, svo_triples, sp_pairs, lang, creation_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item.get_id(),
                    item.get_activity_id(),
                    item.get_learner_id(),
                    item.get_package_id(),
                    item.get_pos_counts(),
                    item.get_total_words(),
                    item.get_content_words(),
                    item.get_descriptive_words(),
                    item.get_unique_words(),
                    item.get_long_words(),
                    item.get_noun_phrases(),
                    item.get_svo_triples(),
                    item.get_sp_pairs(),
                    item.get_lang(),
                    item.get_creation_time()
                ))
                connection.commit()
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")

def export_nlp_csv(connection, file_directory, filename):
    csv_path = os.path.join(file_directory, filename)
    try:
        with closing(connection.cursor()) as cursor:
            cursor.execute('SELECT * FROM processed_text_item_t')
            rows = cursor.fetchall()
            headers = [description[0] for description in cursor.description]
            
            # Write to CSV
            with open(csv_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(headers)
                csvwriter.writerows(rows)
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}")

    def __del__(self):
        if self.connection:
            self.connection.close()
