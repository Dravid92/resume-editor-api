# pypdf2, python-docx

# goal is to extract skills , experience , projects and key information from resume.
class FileParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        # code to parse the resume file and extract skills, experience, projects and key information from it.
        return {
            "skills": ["skill1", "skill2"],
            "experience": ["experience1", "experience2"],
            "projects": ["project1", "project2"],
            "key_information": {"name": "John Doe", "email": "john.doe@example.com"}
        }