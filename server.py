# main.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
import PyPDF2
from pattern_recognise import pattern_results
from db_manage import Manage_DB
import json

app = FastAPI()

# Allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_pattern_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        results = pattern_results(text)
        return results
    
def get_pdf_data(file_path):

    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        
        return text
    


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
    # Save the uploaded file
        with open(file.filename, "wb") as f:
            f.write(file.file.read())

        # Process the PDF file
        result_dict = extract_pattern_pdf(file.filename)

        return JSONResponse(content=result_dict, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/add_record/")
async def add_record(file: UploadFile = File(...), approval: str = Form(...), pdfData: str = Form(...)):
    try:
        # Save the uploaded file
        with open(file.filename, "wb") as f:
            f.write(file.file.read())

        # Read the PDF file
        pdf_text = get_pdf_data(file.filename)
        pdfData = json.loads(pdfData)

        pdfData["Pdf_Data"] = pdf_text
        pdfData["Pdf_Name"] = file.filename
        pdfData["Approval"] = approval


        db_manager = Manage_DB()  # Initialize the database manager

        print('Creating record..')

        # Add the record to the database
        db_manager.create_record("pdf_records", pdfData)

        success_message = "Record created successfully!"

        return JSONResponse(content={"Message": success_message}, status_code=200)

    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
