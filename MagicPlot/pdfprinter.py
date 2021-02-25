from fpdf import FPDF


class PDF(FPDF):
    def __init__(self, orientation='P', unit='px', format='A4', plot=None, data=None, title=None):
        super(PDF, self).__init__()

        self.orientation = orientation
        self.unit = unit
        self.format = format
        self.plot = plot
        self.data = data
        self.title = title

    def header(self):
        self.image(r'.\ressources\images\logo_sbr.png', 5, 4, 50)
        self.set_font('Helvetica', 'B', 20)
        self.cell(80)
        self.cell(0, 0, self.title, 0, 0, 'C')

    def print_result(self):
        self.add_page()
        self.image(self.plot, 5, 25, 200)
        self.ln(4)
        line_height = self.font_size
        col_width = self.epw / 4
        for key in self.data:
            for item, value in self.data[key].items():
                self.multi_cell(col_width, line_height, value,
                                border=1, align='C', ln=3, max_line_height=self.font_size)
            self.ln(line_height)


dict = {'first': {'col1': 'Frequence', 'col2': 'Niveau'}, 'second': {'Frequence': '37373492.172213644', 'Level': '40.512848196933724'}, '< pyqtgraph.graphicsItems.ROI.ROI object at 0x0000017CB9B2B9D0 >': {'Frequence': '108042651.82570055', 'Level': '38.6989851004103'},
        '< pyqtgraph.graphicsItems.ROI.ROI object at 0x0000017CB9B2B160 >': {'Frequence': '375264820.6831262', 'Level': '45.522565320665095'}, '< pyqtgraph.graphicsItems.ROI.ROI object at 0x0000017CB9B2B5E0 >': {'Frequence': '655696057.7364848', 'Level': '44.78838263873895'}}

pdf = PDF(plot=r'.\test.jpg', data=dict,
          title="Test génération de PDF trop cool")
pdf.set_font("Helvetica", size=10)
pdf.print_result()
pdf.output('test.pdf')
