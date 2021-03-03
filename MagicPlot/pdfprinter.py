import jinja2
import pandas as pd
from weasyprint import HTML

TEMPLATE_FILE = "report.html"


class PDF:
    def __init__(self, plot, data, title, fileName):
        super().__init__()

        self.plot = plot
        self.data = data
        self.title = title
        self.fileName = fileName

        self.df = pd.DataFrame(self.data)
        self.df = self.df.T

    def html_to_pdf(self, html_out):
        html_out = html_out
        HTML(string=html_out, base_url='.').write_pdf(self.fileName, stylesheets=[
            "./templates/report.css", "./templates/bootstrap.min.css"])

    def generate_document(self):
        templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(TEMPLATE_FILE)

        html_out = template.render(title=self.title,
                                   logo="./ressources/images/logo_sbr.png",
                                   plot=self.plot,
                                   values=self.df)

        self.html_to_pdf(html_out)
