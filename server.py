from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pattern_recognise import pattern_results
import PyPDF2

app = FastAPI()

# Allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        # print(len(pdf_reader.pages))
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        results = pattern_results(text)
        # print(results)
        return results
        # return text

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        with open(file.filename, "wb") as f:
            f.write(file.file.read())

        # Read the PDF file
        pdf_text = read_pdf(file.filename)

        return JSONResponse(content=pdf_text, status_code=200)

    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
