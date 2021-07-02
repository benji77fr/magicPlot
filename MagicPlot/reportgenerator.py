import jinja2
import pandas as pd
import htmldocx as htmldocx
import docx as docx

TEMPLATE_FILE = "report.html"


class Report:
    def __init__(self, plot, data, title, file_name):
        super().__init__()

        self.plot = plot
        self.data = data
        self.title = title
        self.new_parser = htmldocx.HtmlToDocx()
        self.file_name = file_name

        self.df = pd.DataFrame(self.data)
        self.df = self.df.T

    def generate_document(self):
        template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(TEMPLATE_FILE)

        html_out = template.render(title=self.title,
                                   logo="./ressources/images/logo_sbr.png",
                                   plot=self.plot,
                                   values=self.df)
        with open("html_out.html", "w") as fh:
            fh.write(html_out)

        self.new_parser.parse_html_file("./html_out.html", self.file_name)
