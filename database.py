"""
    Module for handling data
"""

import csv
import sqlite3
from pathlib import Path

from typing import Dict

db_path = r'data\\staff_db.db'


def handle_csv(p: Path):
    """
        CSV IN format
        LAST NAME FIRST NAME PATRON;BIRTH;JOB
    """

    def split_fio(s: str):
        names = s.split()
        return {
            'first_name': names[1].title(),
            'last_name': names[0].title(),
            'patronymic': names[2].title()
        }

    with open(p) as csv_in:
        reader = csv.DictReader(csv_in, delimiter=';')
        with open('staff.csv', 'w', newline='', encoding='utf-8') as csv_out:
            fieldnames = ['last_name', 'first_name', 'patronymic', 'birth', 'job']
            writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                names = split_fio(row['name'])
                data = { 'last_name': names['last_name'], 'first_name': names['first_name'], 
                          'patronymic':names['patronymic'], 'birth':row['birth'], 'job':row['position']}
                writer.writerow(data)

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.jobs_shorts = {
            'медицинский регистратор': 'медрег.',
            'заведующий отделением врач-стоматолог-хирург': 'хир.',
            'врач-стоматолог-хирург': 'хир.',
            'врач-стоматолог' : 'тер.', 
            'медицинская сестра' : 'м,с',
            'рентгенолаборант' : 'рентген.',
            'врач-стоматолог-терапевт' : 'тер.',
            'уборщик служебных помещений' : 'уб.',
            'врач стоматолог - ортопед': 'орт',
            'зубной врач': 'тер.',
            'гардеробщик': 'гард.'
        }


    def create_tables(self):
        create_scipt = '''
        CREATE TABLE "staff" (
            "id"	INTEGER NOT NULL UNIQUE,
            "first_name"	TEXT NOT NULL,
            "last_name"	TEXT NOT NULL,
            "patronymic"	TEXT,
            "job"	TEXT NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT)
            )
        '''

        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.executescript(create_scipt)


    def insert_from_csv(self, f: str):
        with sqlite3.connect(self.db_name) as conn, open(f, 'r', encoding='utf-8') as csv_in:
            cur = conn.cursor()
            reader = csv.DictReader(csv_in)
            for row in reader:
                data = (row['first_name'], row['last_name'], row['patronymic'], row['job'])
                cur.execute("INSERT INTO staff(first_name, last_name, patronymic, job) VALUES (?,?,?,?)", data)
            conn.commit()

    def search_person(self, search_str: str) -> Dict:

        if self.db_name is None:
            raise ValueError('DB Name cannot be None')

        with sqlite3.connect(self.db_name) as conn:
            try:
                strings = search_str.split()
                last_name, first_name = strings[0], ''
                if len(strings) == 2:
                    first_name = strings[1]
            except ValueError:
                print(f'Error with {search_str}')
            cur = conn.cursor()
            res = cur.execute('SELECT * FROM staff WHERE last_name=?', (last_name,)).fetchall()
            if res is None:
                raise Exception(f'Not found {search_str}')
            
            for row in res:
                if first_name in row[1]:
                    return {
                        "first_name": row[1],
                        'last_name': row[2],
                        "patronymic": row[3], 
                        'job': row[4]
                    }

    def get_short_job(self, person: Dict) -> str:
        """
            Returns string with a short job from given Person
        """
        job = person['job'].lower()
        return self.jobs_shorts[job]
        
            

if __name__ == '__main__':
    
    print('database module')
    db = r'res\\staff_db.db'
    with sqlite3.connect(db) as conn, open('staff_out.txt', 'w', encoding='utf-8') as out:
        cur = conn.cursor()
        rows = cur.execute('select * from staff').fetchall()
        for row in rows:
            s = ' '.join(map(str, row)) + '\n'
            out.write(s)

            
    
    