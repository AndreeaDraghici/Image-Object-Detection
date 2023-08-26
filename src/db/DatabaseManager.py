import logging
import sqlite3

from src.LoadLoggingConfig import load_logging_config


class DatabaseManager :
    def __init__(self) :
        load_logging_config()
        # Initialize logger using the specified name
        self.logger = logging.getLogger('development')

        try :
            # Establish a connection to the SQLite database
            self.conn = sqlite3.connect('../db/detected_objects.db')
            self.cursor = self.conn.cursor()

            # Create a table if it doesn't exist to store detected objects
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS detected_objects (
                    id INTEGER PRIMARY KEY,
                    object_type TEXT,
                    x INTEGER,
                    y INTEGER,
                    w INTEGER,
                    h INTEGER,
                    confidence REAL
                )
            ''')
            # Commit the changes to the database
            self.commit_changes()

        except Exception as e :
            # Log an error if any exception occurs during database initialization
            self.logger.error("An error occurred during database initialization:", str(e))

    def insert_detected_objects(self, detected_objects) :
        """
                Insert detected objects and their coordinates into the database.

                :param detected_objects: List of tuples containing object type and coordinates
        """
        try :
            # Iterate through detected objects and insert them into the database
            for obj_label, coords, confidence in detected_objects :
                x, y, w, h = coords

                # Insert the object information into the database
                self.cursor.execute(
                    "INSERT INTO detected_objects (object_type, x, y, w, h, confidence) VALUES (?, ?, ?, ?, ?, ?)",
                    (obj_label, x, y, w, h, confidence))

                # Commit changes and close the connection
            self.commit_changes()

        except Exception as e :
            # Log an error if any exception occurs during insertion
            self.logger.error("An error occurred during inserting detected objects:", str(e))

    def close_connection(self) :
        try :
            # Close the database connection
            self.conn.close()
        except Exception as e :
            # Log an error if any exception occurs during connection closing
            self.logger.error("An error occurred during closing connection:", str(e))

    def commit_changes(self) :
        try :
            # Commit the database changes
            self.conn.commit()
        except Exception as e :
            # Log an error if any exception occurs during commit the changes
            self.logger.error("An error occurred during commit the changes on database:", str(e))
