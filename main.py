from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Field, Session, SQLModel, create_engine, select



class Experience(SQLModel, table=True):
    id: int | None =Field(default=None, primary_key=True)
    title: str = Field(index=True)
    company: str = Field(index=True)
# In-memory storage

skills = []
formation=[]

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

''''
@app.get("/", response_class=HTMLResponse)
def home(request: Request, session: SessionDep):
    experiences = session.exec(select(Experience)).all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "experiences": experiences,
            "skills": skills,
            "formations": formation,

        },
    )
'''
@app.get("/", response_class=HTMLResponse)
def home(request: Request, session: SessionDep):
    experiences = session.exec(select(Experience)).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "experiences": experiences,
            "skills": skills,
            "formations": formation,
        },
    )

'''
@app.post("/add_experience")
def add_experience(experience: Experience, session: SessionDep) -> Experience:
    session.add(experience)
    session.commit()
    session.refresh(experience)
    return experience
'''
@app.post("/add_experience")
def add_experience(
    session: SessionDep,
    title: str = Form(...),
    company: str = Form(...),
    
    ):
    experience = Experience(title=title, company=company)
    session.add(experience)
    session.commit()

    return RedirectResponse(url="/", status_code=303)

@app.post("/add_skill")
def add_skill(skill: str = Form(...)):
    skills.append(skill)
    return RedirectResponse(url="/", status_code=303)


@app.post("/add_formation")
def add_formation(school: str = Form(...), degree: str = Form(...), date_of_graduation: str = Form(...)):
    formation.append({"school": school, "degree": degree, "date_of_graduation": date_of_graduation})
    return RedirectResponse(url="/", status_code=303)