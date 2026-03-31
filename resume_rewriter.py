import json
import re
from typing import Dict


class TemplateLoader:
    def __init__(self, template_path: str):
        self.template_path = template_path

    def load(self) -> str:
        with open(self.template_path, "r", encoding="utf-8") as file:
            return file.read()


class PlaceholderEngine:
    PLACEHOLDER_PATTERN = r"\{\{(.*?)\}\}"

    def __init__(self, template: str):
        self.template = template

    def extract_placeholders(self):
        return set(re.findall(self.PLACEHOLDER_PATTERN, self.template))

    def render(self, data: Dict[str, str]) -> str:
        rendered = self.template

        placeholders = self.extract_placeholders()

        for key in placeholders:
            value = data.get(key, "")

            # Ensure string conversion
            if value is None:
                value = ""

            rendered = rendered.replace(f"{{{{{key}}}}}", str(value))

        return rendered


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
        self.loader = TemplateLoader(template_path)
        self.template = self.loader.load()
        self.engine = PlaceholderEngine(self.template)

    def render(self, json_data: Dict[str, str]) -> str:
        return self.engine.render(json_data)

    def save(self, output_path: str, content: str):
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(content)
