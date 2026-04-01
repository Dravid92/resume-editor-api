class BaseSectionGenerator:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, prompt):
        json = self.llm.generate(prompt)
        return json

class IntroGenerator(BaseSectionGenerator):

    def run(self, resume_text, jd_text):
        prompt = f"""
Use Resume Text and JD Text given below given below to Generate ONLY the "summary" field.

Constraints:
- Max 80 words
- ATS optimized
- Concise and impactful

Return EXACT JSON:
{{
  "summary": "..."
}}

Do NOT add extra keys.

Resume Text:
{resume_text}

JD Text:
{jd_text}
"""
        return self.generate(prompt)

class SkillsGenerator(BaseSectionGenerator):

    def run(self, resume_text, jd_text):
        prompt = f"""
Use Resume Text and JD Text given below to Extract and optimize skills.

Constraints:
- languages: max 12 words
- frameworks: max 12 words
- databases: max 10 words
- cloud_infra: max 10 words
- systems: max 10 words
- practices: max 10 words

Return EXACT JSON:
{{
  "languages": "...",
  "frameworks": "...",
  "databases": "...",
  "cloud_infra": "...",
  "systems": "...",
  "practices": "..."
}}

Do NOT add extra keys.
Resume Text:
{resume_text}

JD Text:
{jd_text}
"""
        return self.generate(prompt)



class ProjectsGenerator(BaseSectionGenerator):

    def run(self, resume_text, jd_text):
        prompt = f"""
Use Resume Text and JD Text given below to Generate project section.

Constraints:
- Name: max 5 words
- Stack: max 8 words
- Description: max 25 words

Return EXACT JSON:

{{
  "project_name_1": "...",
  "project_stack_1": "...",
  "project_link_1": "...",
  "project_description_1": "...",

  "project_name_2": "...",
  "project_stack_2": "...",
  "project_link_2": "...",
  "project_description_2": "..."
}}

Rules:
- No extra keys
- Fill missing fields with ""
Resume Text:
{resume_text}

JD Text:
{jd_text}
"""
        return self.generate(prompt)

class ExperienceGenerator(BaseSectionGenerator):

    def run(self, resume_text, jd_text):
        prompt = f"""
Use Resume Text and JD Text given below to Generate experience section.

Constraints:
- Titles: max 6 words
- Company: max 6 words
- Dates: max 4 words
- Location: max 4 words
- Bullet points: max 20 words each
- Strong action + impact

Return EXACT JSON:

{{
  "experience_title_1": "...",
  "experience_company_1": "...",
  "experience_date_1": "...",
  "experience_location_1": "...",
  "experience_1_bullets_1": "...",
  "experience_1_bullets_2": "...",
  "experience_1_bullets_3": "...",
  "experience_1_bullets_4": "...",

  "experience_title_2": "...",
  "experience_company_2": "...",
  "experience_date_2": "...",
  "experience_location_2": "...",
  "experience_2_bullets_1": "...",
  "experience_2_bullets_2": "...",
  "experience_2_bullets_3": "...",
  "experience_2_bullets_4": "..."
}}

Rules:
- Do NOT skip keys
- Use empty string "" if missing
Resume Text:
{resume_text}

JD Text:
{jd_text}
"""
        return self.generate(prompt)

class HeaderGenerator(BaseSectionGenerator):

    def run(self, resume_text, jd_text):
        prompt = f"""
Use Resume Text given below to Extract personal details.

Constraints:
- company_name_title: max 6 words
- first_name: max 2 words
- last_name: max 2 words
- job_tagline: max 6 words
- email, phone, linkedin, github, location

Return EXACT JSON:

{{
  "company_name_title": "...",
  "first_name": "...",
  "last_name": "...",
  "job_tagline": "...",
  "email": "...",
  "phone": "...",
  "linkedin": "...",
  "github": "...",
  "location": "..."
}}
Resume Text:
{resume_text}
"""
        return self.generate(prompt)

class EducationGenerator(BaseSectionGenerator):

    def run(self, resume_text: str):
        prompt = f"""
            Extract education details from the resume.
            
            Fields:
            - education_degree
            - education_school
            - education_date
            - education_gpa
            
            Constraints:
            - degree: max 8 words
            - school: max 6 words
            - date: max 4 words
            - gpa: max 2 words
            
            Rules:
            - Return ONLY JSON
            - Do NOT add extra keys
            - Use empty string "" if missing
            - Ensure valid JSON
            
            Return EXACT format:
            
            {{
              "education_degree": "...",
              "education_school": "...",
              "education_date": "...",
              "education_gpa": "..."
            }}
            
            Resume:
            {resume_text}
            """
        return self.generate(prompt)
class ResumeOrchestrator:

    def __init__(self, llm):
        self.header = HeaderGenerator(llm)
        self.intro = IntroGenerator(llm)
        self.skills = SkillsGenerator(llm)
        self.exp = ExperienceGenerator(llm)
        self.projects = ProjectsGenerator(llm)
        self.education = EducationGenerator(llm)

    def generate(self, resume_text, jd_text):

        result = {}

        result.update(self.header.run(resume_text))
        result.update(self.intro.run(resume_text, jd_text))
        result.update(self.skills.run(resume_text, jd_text))
        result.update(self.exp.run(resume_text, jd_text))
        result.update(self.projects.run(resume_text, jd_text))

        return result