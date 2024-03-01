from schedule import Schedule
from database import Database

schedule_current = (
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
)

if __name__ == '__main__':
    db_path = r'data\\staff_db.db'
    schedule = Schedule(schedule_data=schedule_current)
    database = Database(db_path)
    schedule.register_database(database)
    schedule.generate_schedule_table()
    schedule.generate_schedule_with_pay()