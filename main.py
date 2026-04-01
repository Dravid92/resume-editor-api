import json

from fastapi import UploadFile, File, Form, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime
import os

from fastapi.responses import HTMLResponse

from file_parser import FileParser, ParserFactory
from job_scraper import JDExtractor, JDHTMLExtractor
from llm_service import ResumeOrchestrator
from lmstudio import LMStudioService

from resume_rewriter import ResumeRenderer

app = FastAPI()
UPLOAD_DIR = "uploads"
PROCESSED_DIR = "generated"
TEMPLATE_PATH = "templates"

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
    file: UploadFile = File(...),
    url: str = Form(...)
):
    input_filename = generate_filename(file.filename)
    input_path = os.path.join(UPLOAD_DIR, input_filename)

    content = await file.read()
    with open(input_path, "wb") as f:
        f.write(content)
    output_filename = f"processed_{input_filename}"
    output_path = os.path.join(PROCESSED_DIR, output_filename)
    parser = ParserFactory(file_path=input_path).get_parser()
    details = parser.extract_text(file_path=input_path)
    print("Resume parsed successfully")
    jd_html_soup = JDHTMLExtractor().extract(url=url)
    jd_text = JDExtractor().extract(soup=jd_html_soup)
    print(f"JD extracted successfully {jd_text}")
    print("Passing details to LLM...")
    llm = LMStudioService()
    resume_suggestions = ResumeOrchestrator(llm=llm).generate(resume_text=details, jd_text=jd_text)
    print("Suggestions extracted successfully from LLM...")
    renderer = ResumeRenderer(TEMPLATE_PATH)
    final_html = renderer.render(resume_suggestions)
    # print(resume_suggestions)
    return HTMLResponse(content=final_html)
