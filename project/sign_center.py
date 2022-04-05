import contextlib
import sqlite3

from elliptic import Point


class SignCenter:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SignCenter, cls).__new__(cls)
        
        return cls.instance

    def __init__(self) -> None:
        self.db_path = 'sign_center.db'

    def _make_query(self, query, data):
        con = sqlite3.connect('sign_center.db')
        cur = con.cursor()
        if data:
            cur.execute(query, data)
        else:
            cur.execute(query)

        result = cur.fetchall()
        con.commit()
        con.close()
        return result

    def register(self, username, password):
        with contextlib.closing(sqlite3.connect(self.db_path)) as connection:
            cursor = connection.cursor()
            login_query = 'INSERT INTO users (username, password) VALUES (?, ?)'
            cursor.execute(login_query, [username, password])

    def login(self, username, password):
        with contextlib.closing(sqlite3.connect(self.db_path)) as connection:
            cursor = connection.cursor()
            login_query = 'SELECT id FROM users WHERE username = ? AND password = ?'
            cursor.execute(login_query, [username, password])
            user_data = cursor.fetchone()
            return user_data[0]

    def set_pulic_key(self, username, password, public_key):
        user_id = self.login(username, password)
        if user_id:
            with contextlib.closing(sqlite3.connect(self.db_path)) as connection:
                cursor = connection.cursor()
                set_public_key_query = 'INSERT INTO public_keys (a, b, p, q, e1_x, e1_y, e2_x, e2_y) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                a, b, p, q, e1, e2 = public_key
                cursor.execute(set_public_key_query, [a, b, p, q, e1.x, e1.y, e2.x, e2.y])
                cursor.execute('SELECT last_insert_rowid()')
                key_id = cursor.fetchone()[0]
                link_user_and_key_query = 'INSERT INTO user_public_key VALUES (?, ?)'
                cursor.execute(link_user_and_key_query, [user_id, key_id])
        

    def get_public_key(self, username):
        with contextlib.closing(sqlite3.connect(self.db_path)) as connection:
            cursor = connection.cursor()
            get_public_key_query = '''SELECT * FROM public_keys WHERE public_keys.id = 
            (SELECT public_key_id FROM user_public_key WHERE user_public_key.user_id = 
                (SELECT user_id FROM users WHERE username = ?))'''
            cursor.execute(get_public_key_query, [username])
            _, a, b, p, q, e1_x, e1_y, e2_x, e2_y = cursor.fetchone()
            e1 = Point(e1_x, e1_y)
            e2 = Point(e2_x, e2_y)
            return a, b, p, q, e1, e2
