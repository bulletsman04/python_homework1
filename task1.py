from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

currentNumber: int = 0
patients: dict = {}


app = FastAPI()

security = HTTPBasic()

class PatientRequest(BaseModel):
    name: str
    surename: str

class PatientReponse(BaseModel):
    id: int
    patient: PatientRequest

@app.get('/')
@app.get('/welcome')
def hello_world():
    return { "message": "Hello World during the coronavirus pandemic!"}

@app.post('/login')
def login(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "trudnY" and credentials.password == "PaC13Nt":
        return RedirectResponse(url='/welcome', status_code=301)
    return "Wrong data"
    

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
def getPatient(id: int):
    if id in patients:
        return patients[id]
    raise HTTPException(status_code=204, detail="Patient not found")

@app.post('/patient')
def patientInfo(patient: PatientRequest):
    global currentNumber
    patientFullInfo = PatientReponse(id = currentNumber, patient = patient)
    patients[currentNumber] = patient
    currentNumber += 1
    return patientFullInfo
