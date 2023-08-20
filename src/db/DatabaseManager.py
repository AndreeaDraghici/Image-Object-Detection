import sqlite3


class DatabaseManager :
    def __init__(self) :
        self.conn = sqlite3.connect('../db/detected_objects.db')
        self.cursor = self.conn.cursor()

        # Creează tabela pentru stocarea datelor dacă nu există
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

    def insert_detected_objects(self, detected_objects) :
        for obj_label, coords in detected_objects :
            x, y, w, h = coords
            self.cursor.execute('INSERT INTO detected_objects (object_type, x, y, w, h) VALUES (?, ?, ?, ?, ?)',
                                (obj_label, x, y, w, h))
        self.conn.commit()

    def close_connection(self) :
        self.conn.close()

    def get_detected_objects(self) :
        self.cursor.execute("SELECT object_type FROM detected_objects")
        detected_objects = self.cursor.fetchall()
        return [row[0] for row in detected_objects]

    def get_object_coordinates(self, obj_label) :
        self.cursor.execute("SELECT x, y, w, h FROM detected_objects WHERE object_type = ?", (obj_label,))
        result = self.cursor.fetchone()
        if result :
            x, y, w, h = result
            return x, y, w, h
        else :
            return None
