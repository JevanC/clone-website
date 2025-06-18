from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from copy_website import generate_website_copy
import uuid
import os

class URLRequest(BaseModel):
    url: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/") 
def read_root():
    return {"message": "Hi Jevan"}

@app.post("/submit-url")
async def submit_url(data: URLRequest):
    
    html_content = await generate_website_copy(data.url)
    os.makedirs("saved_html", exist_ok=True)


    filename = f"{uuid.uuid4().hex}.html"
    filepath = os.path.join("saved_html", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    file_url = f"/saved_html/{filename}"
    app.mount("/saved_html", StaticFiles(directory="saved_html"), name="saved_html")
    return JSONResponse({"file_url": file_url})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)