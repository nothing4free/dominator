import sqlite3
import os

conn = sqlite3.connect('./databases/intel.db')
c = conn.cursor()
c.execute(
    "SELECT * FROM targets;"
)
targets = c.fetchall()

for target in targets:
    os.system("python3 engine.py {}".format(target[0]))