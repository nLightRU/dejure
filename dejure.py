"""
    Module with different utils
"""

import csv
import os
import sqlite3

from docx import Document

db_path = r'data\\staff_db.db'

schedule = [
    '02.03.2024',
    'Жмыров Д',
    'Дюкова Н',
    'Коломлина Г',
    '03.03.2024',
    'Коруняк А',
    'Панарина О',
    'Старкова Т',
    'Романова Е',
    'Макарова Е',
    'Щербакова Л',
    'Кириллова Н',
    '08.03.2024',
    'Антипова Г',
    'Винокурова И',
    'Кирюшина О',
    '09.03.2024',
    'Попов В',
    'Анциферова Н',
    'Буланкина Л',
    'Павлова Т',
    'Булгакова Е',
    'Титова О',
    'Селянин А',
    'Седова Т',
    'Ненашева З',
    '10.03.2024',
    'Новиков А',
    'Перегудова Т',
    'Кульбашная И',
    '16.03.2024',
    'Незнанова К',
    'Винокурова И',
    'Попова Л',
    '17.03.2024',
    'Ворожейкин В',
    'Павлов Д',
    'Ломакина Т',
    'Корягина Н',
    'Мухортова Т',
    'Кочергина Н',
    'Кириллова Н',
    '23.03.2024',
    'Караваева Е',
    'Сенчихина Е',
    'Григорьева Н',
    'Винокурова И',
    'Четырина Н',
    'Сажнева С',
    'Титова О',
    'Ремезов А',
    'Хмырова Ю',
    'Сафонова Н',
    '24.03.2024',
    'Чеканов С',
    'Романова Е',
    'Плотникова Т',
    '30.03.2024',
    'Некрасова А',
    'Попова О',
    'Архипова С',
    '31.03.2024',
    'Ворожейкин В',
    'Жмыров Д',
    'Ковальская Т',
    'Буланкина Л',
    'Васильева Ю',
    'Булгакова Е',
    'Кириллова Н',
]

def handle_csv():

    def split_fio(s: str):
        names = s.split()
        return {
            'first_name': names[1].title(),
            'last_name': names[0].title(),
            'patronymic': names[2].title()
        }

    with open('staff_data.csv') as csv_in:
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
                

def create_db(dbname: str, create_scipt):
    with sqlite3.connect(dbname) as conn:
        cur = conn.cursor()
        cur.executescript(create_scipt)
 

def insert_from_csv(f: str, db: str):
    with sqlite3.connect(db) as conn, open(f, 'r', encoding='utf-8') as csv_in:
        cur = conn.cursor()
        reader = csv.DictReader(csv_in)
        for row in reader:
            data = (row['first_name'], row['last_name'], row['patronymic'], row['job'])
            cur.execute("INSERT INTO staff(first_name, last_name, patronymic, job) VALUES (?,?,?,?)", data)
        conn.commit()

def search_person(name: str):
    with sqlite3.connect(db_path) as conn:
        try:
            last_name, first_name = name.split()
        except ValueError:
            print(f'Error with {name}')
        cur = conn.cursor()
        res = cur.execute('SELECT * FROM staff WHERE last_name=?', (last_name,)).fetchall()
        if res is None:
            raise Exception(f'Not found {name}')
        if len(res) > 1:
            for row in res:
                if first_name in row[1]:
                    return row
        else:
            return res[0]

def create_table_row(person: tuple, date: str):
    name = person[2] + ' ' + person[1][0] + '.' + person[3][0] + '.'
    job = person[4][0].upper() + person[4][1:]
    return {
        'name': name, 
        'job':job,
        'date':date
    }

if __name__ == '__main__':
    
    print('dejure module')
            
    
    