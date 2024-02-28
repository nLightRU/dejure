"""
    Docx generation module
"""
from docx import Document

from dejure import schedule, search_person, create_table_row

def generate_schedule_with_pay():
    schedule_rows = []
    for line in schedule:
        if line[0] in ('0', '1', '2', '3'):
            date = line
            continue
        else:
            person_record = search_person(line)
            table_row = create_table_row(person=person_record, date=date)
            schedule_rows.append(table_row)
        
    document = Document()

    table = document.add_table(rows=1, cols = 3)
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

    document.save('demo_pay.docx')

if __name__ == '__main__':
    print('docx generation module')
    