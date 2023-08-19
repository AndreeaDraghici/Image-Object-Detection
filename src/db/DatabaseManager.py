import sqlite3


class DatabaseManager :
    def __init__(self) :
        self.conn = sqlite3.connect('../db/detected_objects.db')
        self.cursor = self.conn.cursor()

        # Creează tabela pentru stocarea datelor dacă nu există
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS detected_objects (
                id INTEGER PRIMARY KEY,
                object_type TEXT
            )
        ''')
        self.conn.commit()

    def insert_detected_objects(self, detected_objects) :
        for obj_type in detected_objects :
            self.cursor.execute('INSERT INTO detected_objects (object_type) VALUES (?)', (obj_type,))
        self.conn.commit()

    def close_connection(self) :
        self.conn.close()
