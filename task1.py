from fastapi import FastAPI, HTTPException, Depends, Cookie,Response, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from hashlib import sha256
from fastapi.templating import Jinja2Templates

currentNumber: int = 0
patients: dict = {}


app = FastAPI()
app.secret_key = "secretsssssssssssssssssssssssssdfdsfdsgfdhdfh"
app.tokens = []

security = HTTPBasic()

templates = Jinja2Templates(directory="templates")

class PatientRequest(BaseModel):
    name: str
    surename: str

class PatientReponse(BaseModel):
    id: int
    patient: PatientRequest

def check_token(session_token: str = Cookie(None)):
    if session_token not in app.tokens :
        raise HTTPException(status_code=401, detail="Unathorised")


@app.get('/')
def hello_world(session_token: str = Cookie(None)):
        { "message": "Hello World during the coronavirus pandemic!"}

@app.get('/welcome')
def hello_world_welcome(request: Request, session_token: str = Cookie(None)):
    check_token(session_token)
    return templates.TemplateResponse("index.html", {"request": request, "user": app.user}) 


@app.post('/login')
def login(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "trudnY" and credentials.password == "PaC13Nt":
        app.user = credentials.username
        session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
        response = RedirectResponse(url='/welcome', status_code=301)
        response.set_cookie(key="session_token", value=session_token)
        app.tokens.append(session_token)
        return response
    raise HTTPException(status_code=401, detail="Unathorised")

@app.post('/logout')
def logout(session_token: str = Cookie(None)):
    check_token(session_token)
    app.tokens.remove(session_token)
    response = RedirectResponse(url='/', status_code=301)
    app.user = None
    return response
    

@app.get('/method')
def methodGet():
    return {"method": "GET"}

@app.post('/method')
def methodPost():
    return {"method": "POST"}

@app.put('/method')
def methodPut():
    return {"method": "PUT"}

@app.delete('/method')
def methodDelete():
    return {"method": "DELETE"}

@app.get('/patient/{id}')
def getPatient(id: int, session_token: str = Cookie(None)):
    check_token(session_token)
    if id in patients:
        return patients[id]
    raise HTTPException(status_code=204, detail="Patient not found")

@app.post('/patient')
def patientInfo(patient: PatientRequest, session_token: str = Cookie(None)):
    check_token(session_token)
    global currentNumber
    patientFullInfo = PatientReponse(id = currentNumber, patient = patient)
    patients[currentNumber] = patient
    currentNumber += 1
    return patientFullInfo
