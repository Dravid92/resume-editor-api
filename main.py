from fastapi import UploadFile, File, Form, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime
import os

from file_parser import FileParser, ParserFactory
from job_scraper import JDExtractor, JDHTMLExtractor

from ollama import LLMService, OllamaLLM

app = FastAPI()
UPLOAD_DIR = "uploads"
PROCESSED_DIR = "generated"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (dev only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "Hello World"}



def generate_filename(original_name: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(original_name)
    return f"{name}_{timestamp}{ext}"
@app.post("/upload_file")
async def process_upload_file(
    resume: UploadFile = File(...),
    job_url: str = Form(...)
):
    input_filename = generate_filename(resume.filename)
    input_path = os.path.join(UPLOAD_DIR, input_filename)

    content = await resume.read()
    with open(input_path, "wb") as f:
        f.write(content)
    output_filename = f"processed_{input_filename}"
    output_path = os.path.join(PROCESSED_DIR, output_filename)
    parser = ParserFactory(file_path=input_path).get_parser()
    details = parser.extract_text(file_path=input_path)
    jd_html_soup = JDHTMLExtractor().extract(url=job_url)
    jd_text = JDExtractor().extract(soup=jd_html_soup)
    llm = OllamaLLM()
    resume_suggestions = LLMService(llm=llm).suggest_resume_improvements(resume_text=details, job_description=jd_text)
    print(resume_suggestions)
    return {
        "download_url": f"http://127.0.0.1:8000/generated/{output_filename}"
    }
