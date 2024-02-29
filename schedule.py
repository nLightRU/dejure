"""
    Docx generation module
"""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT

class Schedule:
    def __init__(self, schedule_data, database):
        self.schedule = schedule_data
        self.db = database

    def __create_schedule_rows(self):
        schedule_rows = []
        for line in self.schedule:
            if line[0] in ('0', '1', '2', '3'):
                date = line
                continue
            else:
                person_record = self.db.search_person(line)
                table_row = self.db.create_table_row(person=person_record, date=date)
                schedule_rows.append(table_row)
        return tuple(schedule_rows)
    
    def generate_schedule_with_pay(self, filename='demo_pay.docx'):
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

    def generate_schedule_table(self, filename='demo_table.docx'):

        document = Document()
        
        heading = document.add_heading('График дежурств', level=1)
        heading.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        table = document.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.style = 'Table Grid'
        for i in range(5):
            row_cells = table.rows[i].cells
            
            row_cells[0].add_paragraph('first', style='List Number')
            row_cells[0].add_paragraph('second', style='List Number')
            row_cells[0].add_paragraph('third', style='List Number')
            
            row_cells[1].add_paragraph('first', style='List Number')
            row_cells[1].add_paragraph('second', style='List Number')
            row_cells[1].add_paragraph('third', style='List Number')
            
            table.add_row()
            
        document.save(filename)
        

if __name__ == '__main__':
    print('docx generation module')
    