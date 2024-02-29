import pytest

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

    with sqlite3.connect('test_database.db') as conn:
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS staff')
        cur.execute(create_script)
        for person in persons:
            cur.execute(insert_script, person)
        conn.commit()
    
    db = Database(db_name='test_database.db')

    return db

@pytest.fixture
def test_persons():
    persons = (
        {'first_name': 'Евгений','last_name': 'Базаров','patronymic':'Васильевич', 'job': 'стоматолог-терапевт'},
        {'first_name': 'Анна', 'last_name': 'Одинцова', 'patronymic': 'Сергеевна', 'job':'медицинская сестра'},
        {'first_name':'Павел', 'last_name':'Кирсанов', 'patronymic': 'Петрович', 'job':'стоматолог-терапевт'},
        {'first_name':'Авдотья', 'last_name':'Кукшина', 'patronymic': 'Никитична', 'job':'уборщица'},
        {'first_name':'Иван', 'last_name':'Иванов', 'patronymic': 'Иванович', 'job':'стоматолог-хирург'}
    )

    return persons

def test_get_person(test_db, test_persons):
    for test_p in test_persons:
        search_q = test_p['last_name'] + ' ' + test_p['first_name'][0]
        p = test_db.search_person(search_q)
        res = p['last_name'] == test_p['last_name']
        assert res is True, "Can't search"
