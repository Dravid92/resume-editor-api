from jinja2 import Environment, FileSystemLoader
from typing import Dict


class TemplateLoader:
    def __init__(self, template_path: str):
        self.template_path = template_path

    def load(self) -> str:
        with open(self.template_path, "r", encoding="utf-8") as file:
            return file.read()



class HTMLRenderer:
    def __init__(self, template_path: str):
        template_loader = FileSystemLoader(searchpath=template_path)
        self.env = Environment(loader=template_loader, autoescape=True)

    def render(self, template_name: str, context: dict, output_path: str):
        template = self.env.get_template("template.html")

        rendered_html = template.render(context)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)

        return rendered_html

class ResumeValidator:
    def __init__(self, required_fields=None):
        self.required_fields = required_fields or []

    def validate(self, data: Dict[str, str]):
        missing = []

        for field in self.required_fields:
            if field not in data:
                missing.append(field)

        return missing


class ResumeRenderer:
    def __init__(self, template_path: str):
        self.engine = HTMLRenderer(template_path)

    def render(self, json_data: Dict[str, str]) -> str:
        return self.engine.render(context=json_data, template_name="template", output_path="output/output.html")

    def save(self, output_path: str, content: str):
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(content)
        return file
