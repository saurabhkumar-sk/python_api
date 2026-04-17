from fastapi import FastAPI
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
