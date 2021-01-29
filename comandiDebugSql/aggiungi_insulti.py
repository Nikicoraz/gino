import sqlite3
from typing import Pattern
import re

conn = sqlite3.connect('generale.db')
c = conn.cursor()

insulti = []
pattern = r'[a-zA-Z0-9 ]+'
while True:
    i = input('Inserire insulto: ')
    if i.strip().lower() == 'fine':
        break
    if re.match(pattern, i):
        insulti.append(i)
    else:
        print('Insulto con caratteri strani!')

for i in insulti:
    c.execute(f"INSERT INTO insulti VALUES ('{i}')")
conn.commit()
conn.close()
