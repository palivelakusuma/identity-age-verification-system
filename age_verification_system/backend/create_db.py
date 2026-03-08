import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id TEXT PRIMARY KEY,
fingerprint TEXT,
dob TEXT
)
""")

users = [
("UID1001","1234","2000-05-15"),
("UID1002","5678","2010-09-21")
]

cursor.executemany(
"INSERT OR REPLACE INTO users VALUES(?,?,?)",
users
)

conn.commit()
conn.close()

print("Database created successfully")