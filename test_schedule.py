import pytest

from schedule import Schedule

@pytest.fixture
def test_db():
    import sqlite3
    from database import Database

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
        ('Анна','Одинцова','Сергеевна','медицинская сестра'),
        ('Павел','Кирсанов','Петрович','стоматолог-терапевт'),
        ('Авдотья','Кукшина','Никитична','уборщица'),
        ('Иван','Иванов','Иванович','стоматолог-хирург')
    )

    with sqlite3.connect('db_test.db') as conn:
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS staff')
        cur.execute(create_script)
        for person in persons:
            cur.execute(insert_script, person)
        conn.commit()
    
    db = Database(db_name='db_test.db')

    return db

@pytest.fixture
def test_schedule():
    test_schedule = (
        '01.01.2024',
        'Базаров Е',
        'Одинцова А',
        '02.01.2024',
        'Кирсанов П',
        'Кукшина А',
        'Иванов И'
    )
    return test_schedule

def test_generate_schedule_table(test_schedule, test_db):
    sc = Schedule(test_schedule)
    sc.register_database(test_db)

    sc.generate_schedule_table()

def test_generate_schedule_with_pay(test_schedule, test_db):
    sc = Schedule(test_schedule)
    sc.register_database(test_db)

    sc.generate_schedule_with_pay()