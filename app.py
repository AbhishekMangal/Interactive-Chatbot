from fastapi import FastAPI, Form, Request, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn
import os
from pathlib import Path
from src.helper import ChatBot  # ChatBot should handle both URLs and PDF paths

# --- Configuration ---
UPLOAD_DIR = Path("./static/docs")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

# Store chain per session (host-based, non-persistent)
session_chains = {}


@app.get("/")
async def index(request: Request):
    """Render main frontend page."""
    return templates.TemplateResponse("frontend.html", {"request": request})


@app.post("/set_url")
async def set_url(request: Request, url: str = Form(...)):
    """Process a URL and store the ChatBot instance for this session."""
    try:
        chain = ChatBot(url)
        session_chains[request.client.host] = chain
        return JSONResponse(content=jsonable_encoder({"msg": "URL processed successfully."}))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing URL: {str(e)}")



@app.post("/set_pdf")
async def set_pdf(request: Request, pdf: UploadFile = File(...)):
    """
    Accept a PDF upload, save it locally, and pass its path to ChatBot.
    """
    try:
        # Validate file type
        if not pdf.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        # Save PDF to uploads directory
        file_path = UPLOAD_DIR / pdf.filename
        with open(file_path, "wb") as f:
            f.write(await pdf.read())

        # Create ChatBot instance using PDF path
        chain = ChatBot(str(file_path))
        session_chains[request.client.host] = chain

        # Delete the file after preprocessing
        try:
            file_path.unlink()
        except Exception as cleanup_err:
            print(f"Warning: could not delete {file_path}: {cleanup_err}")

        return JSONResponse(
            content=jsonable_encoder({"msg": "PDF processed successfully."})
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")



@app.post("/ask")
async def ask_question(request: Request, question: str = Form(...)):
    """Ask a question to the current session's ChatBot chain."""
    client_id = request.client.host
    if client_id not in session_chains:
        raise HTTPException(status_code=400, detail="You must first provide a URL or PDF.")

    chain = session_chains[client_id]
    try:
        result = chain.invoke({"question": question})
        print("DEBUG raw chain output:", result)

        answer = result.get("answer") or result.get("output_text") or "No answer found."
        sources = result.get("sources", "")

        return JSONResponse(content={"answer": answer, "sources": sources})
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
