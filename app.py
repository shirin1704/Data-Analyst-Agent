# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fastapi",
#     "python-multipart",
#     "uvicorn",
#     "google-genai",
#     "python-dotenv",
# ]
# ///

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def task_breakdown(task:str):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    task_breakdown_file = os.path.join('prompts', 'task_breakdown.txt')
    with open(task_breakdown_file, 'r') as file:
        task_breakdown_prompt = file.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents = [task, task_breakdown_prompt],
    )

    with open('task_broken.txt', 'w') as file:
        file.write(response.text)

    return response.text

@app.get("/")
async def root():
    return {"message": "Hello!"}

@app.post("/api/")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = content.decode("utf-8")
        breakdown = task_breakdown(text)
        #print(breakdown)
        return {"filename": file.filename, "content": text}
    except Exception as e:
        return JSONResponse(status_code = 400, content = {"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)