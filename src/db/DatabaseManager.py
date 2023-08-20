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
                    h INTEGER
                )
            ''')
            # Commit the changes to the database
            self.conn.commit()
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
            for obj_label, coords in detected_objects :
                x, y, w, h = coords
                self.cursor.execute('INSERT INTO detected_objects (object_type, x, y, w, h) VALUES (?, ?, ?, ?, ?)',
                                    (obj_label, x, y, w, h))
            # Commit the changes to the database
            self.conn.commit()
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

    def get_detected_objects(self) :
        """
              Retrieve a list of detected object types from the database.

              :return: List of detected object types
        """
        try :
            # Execute a query to retrieve the object types of detected objects
            self.cursor.execute("SELECT object_type FROM detected_objects")
            detected_objects = self.cursor.fetchall()
            # Return a list of detected object types
            return [row[0] for row in detected_objects]
        except Exception as e :
            # Log an error if any exception occurs during retrieval
            self.logger.error("An error occurred during retrieving detected objects:", str(e))
            return []

    def get_object_coordinates(self, obj_label) :
        """
            Retrieve the coordinates of a specific object type from the database.

            :param obj_label: Object type
            :return: Coordinates (x, y, w, h) of the specified object type, or None if not found
        """
        try :
            # Execute a query to retrieve the coordinates of a specific object type
            self.cursor.execute("SELECT x, y, w, h FROM detected_objects WHERE object_type = ?", (obj_label,))
            result = self.cursor.fetchone()
            if result :
                # If the object exists, extract and return its coordinates
                x, y, w, h = result
                return x, y, w, h
            else :
                return None
        except Exception as e :
            # Log an error if any exception occurs during retrieval
            self.logger.error("An error occurred during retrieving object coordinates:", str(e))
            return None
