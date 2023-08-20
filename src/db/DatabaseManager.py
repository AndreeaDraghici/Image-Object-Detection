import logging
import sqlite3

from src.LoadLoggingConfig import load_logging_config


class DatabaseManager :
    def __init__(self) :
        load_logging_config()
        self.logger = logging.getLogger('EventDetectionUI')

        try :
            self.conn = sqlite3.connect('../db/detected_objects.db')
            self.cursor = self.conn.cursor()

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS detected_objects (
                    id INTEGER PRIMARY KEY,
                    object_type TEXT,
                    x INTEGER,
                    y INTEGER,
                    w INTEGER,
                    h INTEGER
                )
            ''')

            self.conn.commit()
        except Exception as e :
            self.logger.error("An error occurred during database initialization:", str(e))

    def insert_detected_objects(self, detected_objects) :
        try :
            for obj_label, coords in detected_objects :
                x, y, w, h = coords
                self.cursor.execute('INSERT INTO detected_objects (object_type, x, y, w, h) VALUES (?, ?, ?, ?, ?)',
                                    (obj_label, x, y, w, h))
            self.conn.commit()
        except Exception as e :
            self.logger.error("An error occurred during inserting detected objects:", str(e))

    def close_connection(self) :
        try :
            self.conn.close()
        except Exception as e :
            self.logger.error("An error occurred during closing connection:", str(e))

    def get_detected_objects(self) :
        try :
            self.cursor.execute("SELECT object_type FROM detected_objects")
            detected_objects = self.cursor.fetchall()
            return [row[0] for row in detected_objects]
        except Exception as e :
            self.logger.error("An error occurred during retrieving detected objects:", str(e))
            return []

    def get_object_coordinates(self, obj_label) :
        try :
            self.cursor.execute("SELECT x, y, w, h FROM detected_objects WHERE object_type = ?", (obj_label,))
            result = self.cursor.fetchone()
            if result :
                x, y, w, h = result
                return x, y, w, h
            else :
                return None
        except Exception as e :
            self.logger.error("An error occurred during retrieving object coordinates:", str(e))
            return None
