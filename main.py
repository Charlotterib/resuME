from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# In-memory storage
experiences = []
skills = []
formation=[]

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "experiences": experiences,
            "skills": skills,
            "formations": formation,

        },
    )

@app.post("/add_experience")
def add_experience(title: str = Form(...), company: str = Form(...)):
    experiences.append({"title": title, "company": company})
    return RedirectResponse(url="/", status_code=303)

@app.post("/add_skill")
def add_skill(skill: str = Form(...)):
    skills.append(skill)
    return RedirectResponse(url="/", status_code=303)


@app.post("/add_formation")
def add_formation(school: str = Form(...), degree: str = Form(...), date_of_graduation: str = Form(...)):
    formation.append({"school": school, "degree": degree, "date_of_graduation": date_of_graduation})
    return RedirectResponse(url="/", status_code=303)