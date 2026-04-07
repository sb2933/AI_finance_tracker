from fastapi import FastAPI, UploadFile, File 
from parser.pdf_parser import extract_transactions_from_pdf 
from parser.docx_parser import extract_transactions_from_docx
import os

app = FastAPI() #creates FastAPI app object called app

@app.get("/") #root route
def read_root():
    return {"message": "AI Finance Tracker API", "endpoint": "/upload_pdf"}

@app.post("/upload_pdf") #tells fastapi that this function should handel post req to upload_pdf
async def upload_pdf(file: UploadFile = File(...)): #define asynchronous function
    # Save the uploaded file temporarily
    temp_file = file.filename
    with open(file.filename, "wb") as f: #opens a file in write-binary mode
        f.write(await file.read()) #write uploaded pdf to disk
    #at this point, the pdf exists on my server temporarily 
    # Call  parser function from pdf.py

    if temp_file.endswith(".pdf"):
        transactions = extract_transactions_from_pdf(temp_file)
    if temp_file.endswith(".docx"):
        transactions = extract_transactions_from_docx(temp_file)
    else:
        transcations = []
    
    os.remove(temp_file)

    
    
    return {"transactions": transactions}