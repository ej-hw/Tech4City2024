import os
import sqlite3
import base64
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from model import save_image, classify_image, insert_image_info, convert_image_to_base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Use environment variable for the static files directory
static_dir = os.getenv('STATIC_DIR', 'frontend')
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', static_dir))
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.config = {
    'UPLOAD_FOLDER': os.path.join(static_dir, 'images')
}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def init_db():
    db_path = 'database.db'
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                prediction TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    with open(os.path.join(static_dir, 'index.html')) as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/upload", response_class=JSONResponse)
async def upload(request: Request, imagefile: UploadFile = File(...)):
    prediction = None
    image_data = None

    if imagefile.filename == '':
        return JSONResponse(content={"prediction": "", "image_data": ""})

    if imagefile:
        # Save the uploaded file
        filepath = save_image(imagefile, app.config['UPLOAD_FOLDER'])

        # Classify the image
        prediction = classify_image(filepath)

        # Insert image info and prediction into the database
        insert_image_info(imagefile.filename, filepath, prediction)

        # Convert image to base64
        image_data = convert_image_to_base64(filepath)

    return JSONResponse(content={"prediction": prediction, "image_data": image_data})

@app.get("/history", response_class=HTMLResponse)
async def history(request: Request):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT name, path, prediction FROM images')
    records = c.fetchall()
    conn.close()

    # Serve the history.html with the records data
    with open(f"{static_dir}/history.html", "r") as file:
        html_content = file.read()
        records_html = ""
        for record in records:
            records_html += f"""
            <tr>
                <td>{record[0]}</td>
                <td>{record[2]}</td>````
                <td><img src="/static/images/{record[0]}" class="img-thumbnail" width="100"></td>
            </tr>
            """
        html_content = html_content.replace("{{ records }}", records_html)

    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)