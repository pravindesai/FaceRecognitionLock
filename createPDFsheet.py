from datetime import datetime

from fpdf import FPDF
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Students']
user = db.user
col_name = 'day' + str(datetime.now().strftime('%d_%m_%Y'))
attendance = db[col_name]
pdf = FPDF()

pdf.add_page(orientation='P')

pdf.set_font("Arial", 'B', size=10)
pdf.cell(180, 15, txt=col_name, ln=1, align="C")
pdf.set_font("Arial", size=10)

for i in range(1, attendance.count_documents({}) + 1):
    id = str(attendance.find_one({'id': str(i)}, {'id': 1})['id']) + ' ' * 20
    name = str(user.find_one({'id': str(i)}, {'name': 1})['name'])
    name = name + ' ' * (30 - len(name))
    val = str(attendance.find_one({'id': str(i)}, {'val': 1})['val'])

    print(id + name + val)
    pdf.cell(100, 5, txt='-' * 280, ln=i, align="C")
    pdf.cell(100, 5, txt=id + name + val, ln=i, align="C")

pdf.set_font("Arial", 'I', size=4)
pdf.cell(100, 5, txt='**END' * 280, align="C")
pdf.output("./PDFSHEET/" + col_name + ".pdf")
