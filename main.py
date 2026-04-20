from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

def get_patient():
    with open("patient.json","r") as f :
        data = json.load(f)
    return data    
    
@app.get("/")
def hello():
    return {"status" : True, "message" : "Hello World"}


@app.get("/about")
def print_about():
    return {"status" : True, "message" : "Hello i'am learning python"}


@app.get('/view_user')
def view_user():
    data = get_patient()
    return data

@app.get("/patient/{user_id}")
def get_pat(user_id : int):
    data = get_patient()

    for patient in data['patients']:
        if(patient['id'] == user_id):
            return {"status": True, "patient" : patient}
        else:
            return {"status":False, "detail":"Patient not found"}
        
    raise HTTPException(status_code=404, detail="Patient not found")
