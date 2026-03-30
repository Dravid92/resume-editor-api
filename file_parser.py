# pypdf2, python-docx
import pdfplumber
from docx import Document


class ParserFactory:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_parser(self):
        if self.file_path.endswith(".pdf"):
            return PDFParser()
        elif self.file_path.endswith(".docx"):
            return DOCXParser()
        else:
            raise ValueError("Unsupported file type")
# goal is to extract skills , experience , projects and key information from resume.
class FileParser:
    def __init__(self):
        pass
    def extract_text(self, file_path: str):
        # code to parse the resume file and extract skills, experience, projects and key information from it.
        raise NotImplementedError

class PDFParser(FileParser):
    def extract_text(self, file_path):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

class DOCXParser(FileParser):
    def extract_text(self, file_path):
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text

class SkillsExtractor:

    def extract(self, text: str):
        skills_keywords = ["python", "django", "fastapi", "sql", "aws"]
        return [s for s in skills_keywords if s in text.lower()]

class ExperienceExtractor:

    def extract(self, text: str):
        return self._extract_section(text, "experience")

    def _extract_section(self, text, section):
        lines = text.split("\n")
        result = []
        capture = False

        for line in lines:
            if section in line.lower():
                capture = True
                continue
            if capture:
                if not line.strip():
                    break
                result.append(line.strip())

        return result