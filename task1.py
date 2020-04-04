from fastapi import FastAPI

from pydantic import BaseModel

currentNumber: int = 0

app = FastAPI()

class PatientRequest(BaseModel):
    name: str
    surename: str

class PatientReponse(BaseModel):
    id: int
    patient: PatientRequest

@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

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

@app.post('/patient')
def patientInfo(patient: PatientRequest):
    global currentNumber
    patientFullInfo = PatientReponse(id = currentNumber, patient = patient)
    currentNumber += 1
    return patientFullInfo