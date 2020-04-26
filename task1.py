from fastapi import FastAPI, HTTPException, Depends, Cookie,Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from hashlib import sha256

currentNumber: int = 0
patients: dict = {}


app = FastAPI()
app.secret_key = "secretsssssssssssssssssssssssssdfdsfdsgfdhdfh"
app.tokens = []

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
        session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}")).hexdigest()
        response = RedirectResponse(url='/welcome', status_code=301)
        response.set_cookie(key="session_token", value=session_token)
        app.tokens.add(session_token)
        return response
    raise HTTPException(status_code=401, detail="Unathorised")
    

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
