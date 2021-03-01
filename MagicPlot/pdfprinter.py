# from fpdf import FPDF


# class PDF(FPDF):
#     def __init__(self, orientation='P', unit='px', format='A4', plot=None, data=None, title=None):
#         super(PDF, self).__init__()

#         self.orientation = orientation
#         self.unit = unit
#         self.format = format
#         self.plot = plot
#         self.data = data
#         self.title = title

#     def header(self):
#         self.image(r'.\ressources\images\logo_sbr.png', 5, 4, 50)
#         self.set_font('Helvetica', 'B', 20)
#         self.cell(80)
#         self.cell(0, 0, self.title, 0, 0, 'C')

#     def print_result(self):
#         self.add_page()
#         self.image(self.plot, 5, 25, 200)
#         self.cell(3, 0, self.plot)
#         self.ln(4)
#         line_height = self.font_size
#         col_width = self.epw / 4
#         for key in self.data:
#             for item, value in self.data[key].items():
#                 self.cell(col_width, line_height, value,
#                           border=1, align='C')
#             self.ln(line_height)


# pdf = PDF(plot=r'.\test.jpg', data=dict,
#           title="Test génération de PDF trop cool")
# pdf.set_font("Helvetica", size=10)
# pdf.print_result()
# pdf.output('test.pdf')

# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import cm
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import Paragraph, Frame, Table, Spacer, TableStyle
# from PIL import Image
# import pandas as pd

# class PDF():
#     def __init__(self, fileName, plot, data, title):
#         super().__init__()

#         self.plot = plot
#         self.data = data
#         self.title = title
#         self.pdf = canvas.Canvas(fileName, pagesize=A4)
#         self.docWidth, self.docHeight = A4

#     def data_to_table(self):
#         df = pd.DataFrame(self.data)
#         df = df.T

#         dfToList = [df.columns.to_list()] + df.values.tolist()
#         table = Table(dfToList)
#         table.setStyle(TableStyle([
#             ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
#             ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
#         ]))

#         self.table_value = [Paragraph("Valeurs relevées", getSampleStyleSheet()['Heading1']),
#                             Spacer(1, 20),
#                             table]

#     def construct_pdf(self):
#         self.pdf.translate(cm, cm)

#         imageDfile = Image.open(self.plot)
#         imageWidth, imageHeight = imageDfile.size
#         imageAspect = imageHeight / float(imageWidth)

#         printWidth = self.docWidth
#         printHeight = self.docHeight * imageAspect

#         self.pdf.drawImage(
#             r'.\ressources\images\logo_sbr.png', 2, 750, 108, 25)
#         self.pdf.setFont('Helvetica', 20)
#         self.pdf.drawCentredString(
#             250, 700, self.title)
#         self.pdf.drawImage(self.plot, 2, 400, 700, 350,
#                            preserveAspectRatio=True)

#         f = Frame(cm, cm, 15*cm, 9*cm)
#         f.addFromList(self.table_value, self.pdf)
#         self.pdf.save()

#     def build_pdf(self):
#         self.data_to_table()
#         self.construct_pdf()


import jinja2
import pandas as pd
from weasyprint import HTML

templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "report.html"
template = templateEnv.get_template(TEMPLATE_FILE)

dict = {'second': {'Frequence': '37373492.172213644', 'Level': '40.512848196933724'}, 'third': {'Frequence': '108042651.82570055', 'Level': '38.6989851004103'},
        'forth': {'Frequence': '375264820.6831262', 'Level': '45.522565320665095'}, 'fifth': {'Frequence': '655696057.7364848', 'Level': '44.78838263873895'}}

df = pd.DataFrame(dict)
df = df.T


html_out = template.render(title="Titre Test PDF générer !!!!",
                logo="./ressources/images/logo_sbr.png",
                plot="./test.jpg",
                values=df.to_html())

HTML(string=html_out, base_url='.').write_pdf("report.pdf", stylesheets=["./templates/report.css", "./templates/bootstrap.css"])