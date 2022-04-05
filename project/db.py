import sqlite3


con = sqlite3.connect('sign_center.db')

cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE users
            (id INTEGER PRIMARY KEY,
            username varchar(20) NOT NULL,
            password varchar(20) NOT NULL)''')

cur.execute('''CREATE TABLE public_keys
            (id INTEGER PRIMARY KEY,
            a INTEGER NOT NULL,
            b INTEGER NOT NULL,
            p INTEGER NOT NULL,
            q INTEGER NOT NULL,
            e1_x INTEGER NOT NULL,
            e1_y INTEGER NOT NULL,
            e2_x INTEGER NOT NULL,
            e2_y INTEGER NOT NULL)''')

cur.execute('''CREATE TABLE user_public_key
            (user_id INTEGER NOT NULL,
            public_key_id INTEGER NOT NULL)''')


# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
