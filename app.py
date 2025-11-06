# app/main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pymysql

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_connection():
    return pymysql.connect(host="localhost", user="root", password="root", database="edudb")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
def search_student(request: Request, name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE %s", (f"%{name}%",))
    result = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("result.html", {"request": request, "data": result})
