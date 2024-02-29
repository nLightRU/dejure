"""
    Docx generation module
"""

from typing import Tuple, Dict

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from database import Database

class Schedule:
    def __init__(self, schedule_data):
        self.schedule = schedule_data
        self.db = None
        self.days_num = 0
        for row in schedule_data:
            if row[0] in ('0', '1', '2', '3'):
                self.days_num += 1
        
        months = ('', 
                  'январь', 'февраль', 'март',
                  'апрель', 'май', 'июнь',
                  'июль', 'август', 'сентябрь',
                  'октябрь', 'ноябрь', 'декабрь',
        )

        if schedule_data[0][3] == '0':
            month_num = int(schedule_data[0][4])
        else:
            month_num = int(schedule_data[0][3:4])
        self.month = months[month_num]
        

    def register_database(self, database: Database):
        self.db = database

    def __create_table_row(self, person: Dict, date: str):
        name = person['last_name'] + ' ' + person['first_name'][0] + '.' + person['patronymic'][0] + '.'
        job = person['job'][0].upper() + person['job'][1:]
        job_short = self.db.get_short_job(person=person)
        return {
            'name': name, 
            'job':job,
            'job_short': job_short,
            'date': date
        }
    
    def __create_schedule_rows(self) -> tuple:
        """
            Selects persons from the database and 
            returns the tuple of dicts like 
            {
                'name':'Иванов А.И.', 
                'job':'Стоматолог-терапевт', 
                'job_short':'тер.', 
                'date':'22.01.2025'
            }
        """
        schedule_rows = []
        for line in self.schedule:
            if line[0] in ('0', '1', '2', '3'):
                date = line
                continue
            else:
                person_record = self.db.search_person(line)
                table_row = self.__create_table_row(person=person_record, date=date)
                schedule_rows.append(table_row)
        return tuple(schedule_rows)
    
    def __create_schedule_days(self) -> Tuple[Dict]:
        schedule_rows = self.__create_schedule_rows()
        dates = []
        days = []

        # creating list with duty dates without persons
        # list dates is needed for filtering same dates
        for schedule_row in schedule_rows:
            if schedule_row['date'] not in dates:
                dates.append(schedule_row['date'])
                days.append(
                    {
                        'date': schedule_row['date'],
                        'persons': []
                    }
                )
        
        # adding person to a specific day in days list
        for schedule_row in schedule_rows:
            for day in days:
                if schedule_row['date'] == day['date']:
                    s = f"{schedule_row['name']} - {schedule_row['job_short']}"
                    day['persons'].append(s)


        return tuple(days)

    def generate_schedule_with_pay(self, filename='demo_pay.docx') -> None:
        schedule_rows = self.__create_schedule_rows()
            
        document = Document()
        
        table = document.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'ФИО'
        hdr_cells[1].text = 'Должность'
        hdr_cells[2].text = 'Дата'

        # hdr_cells[0].style.font.bold = True 

        for i, sc_row in enumerate(schedule_rows, start=1):
            row_cells = table.add_row().cells
            row_cells[0].text = sc_row['name']
            row_cells[1].text = sc_row['job']
            row_cells[2].text = sc_row['date']

        document.save(filename)

    def generate_schedule_table(self, filename='demo_table.docx') -> None:
        """
            row_cells[0].add_paragraph('first', style='List Number')
        """

        document = Document()
        
        heading_text = f'График дежурств на {self.month}'
        heading = document.add_heading(heading_text, level=1)
        heading.alignment = WD_TABLE_ALIGNMENT.CENTER
        

        if self.days_num % 2 == 0:
            t_rows = int(self.days_num / 2)
        else:
            t_rows = int(self.days_num / 2) + 1
        
        table = document.add_table(rows=t_rows, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.style = 'Table Grid'

        days = self.__create_schedule_days()
        text = f'test {self.days_num}'
        col_idx, row_idx = 0, 0
        for day in days:
            cell = table.cell(row_idx, col_idx)
            if col_idx == 1:
                row_idx += 1
                col_idx = 0
            else:
                col_idx = 1
            date_text = cell.add_paragraph(day['date'])
            date_text.style = document.styles['Heading 2']
            date_text.alignment = WD_ALIGN_PARAGRAPH.CENTER
            start = 1
            for p in day['persons']:
                text = str(start) + '.' + '  ' + p
                cell.add_paragraph(text)
                start += 1
            
          
            
        document.save(filename)
        

if __name__ == '__main__':
    print('docx generation module')
    