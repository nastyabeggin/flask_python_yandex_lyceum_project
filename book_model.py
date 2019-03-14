class BookModel:
    def __init__(self, connection):
        self.connection = connection


    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 img  VARCHAR(100),
                                 title VARCHAR(100),
                                 content VARCHAR(1000),
                                 year VARCHAR(100),
                                 name VARCHAR(100)
                                 )''')
        cursor.close()
        self.connection.commit()


    def insert(self, img, title, content, year, name):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO books (img, title, content, year, name) 
                      VALUES (?,?,?,?,?)''', (img, title, content, str(year), name))
        cursor.close()
        self.connection.commit()


    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        return rows


    def delete(self, book_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM books WHERE id = ?''', (str(book_id),))
        cursor.close()
        self.connection.commit()

    def exists(self, title, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books WHERE title = ? AND name = ?",
                       (title, name))
        row = cursor.fetchone()
        if row:
            return True
        else:
            return False

    def is_title_busy(self, title):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM books WHERE title = '{}'".format(str(title)))
        row = cursor.fetchone()
        if row:
            return True
        return False
