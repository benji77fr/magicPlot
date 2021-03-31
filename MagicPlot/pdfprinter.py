import jinja2
import pandas as pd
from weasyprint import HTML

TEMPLATE_FILE = "report.html"


class PDF:
    def __init__(self, plot, data, title, file_name):
        super().__init__()

        self.plot = plot
        self.data = data
        self.title = title
        self.file_name = file_name

        self.df = pd.DataFrame(self.data)
        self.df = self.df.T

    def html_to_pdf(self, html_out):
        html_out = html_out
        HTML(string=html_out, base_url='.').write_pdf(self.file_name, stylesheets=[
            "./templates/report.css", "./templates/bootstrap.min.css"])

    def generate_document(self):
        template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(TEMPLATE_FILE)

        html_out = template.render(title=self.title,
                                   logo="./ressources/images/logo_sbr.png",
                                   plot=self.plot,
                                   values=self.df)

        self.html_to_pdf(html_out)
