import sqlite3

from dejure import search_person, create_table_row

from schedule import Schedule

def create_test_db():
    create_script = '''
    CREATE TABLE "staff" (
        "id"	INTEGER NOT NULL UNIQUE,
        "first_name"	TEXT NOT NULL,
        "last_name"	TEXT NOT NULL,
        "patronymic"	TEXT,
        "job"	TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
        )'''
    
    insert_script = 'INSERT INTO staff(first_name, last_name, patronymic, job) VALUES (?, ?, ?, ?)'
    persons = (
        ('Евгений','Базаров','Васильевич','стоматолог-терапевт'),
        ('Анна','Одинцова','Сергеевна','медсестра'),
        ('Павел','Кирсанов','Петрович','стоматолог-терапевт'),
        ('Авдотья','Кукшина','Никитична','медсестра'),
        ('Иван','Иванов','Иванович','стоматолог-хирург')
    )

    with sqlite3.connect('test_database.db') as conn:
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS staff')
        cur.execute(create_script)
        for person in persons:
            cur.execute(insert_script, person)
        conn.commit()



if __name__ == '__main__':

    create_test_db()

    test_schedule = (
        '01.01.2024',
        'Базаров Е',
        'Одинцова А',
        '02.01.2024',
        'Кирсанов П',
        'Кукшина А',
        'Иванов И'
    )

    sc = Schedule(test_schedule, db_name='test_database.db')
    sc.generate_schedule_table()
    sc.generate_schedule_with_pay()