from fastapi import FastAPI, HTTPException, Query,Request
import json
from pydantic import BaseModel, Field, field_validator , computed_field
from typing import Annotated, Literal
from fastapi.responses  import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

file_name = "patient.json"


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request : Request,exc:RequestValidationError):
    error_msg = exc.errors()[0]["msg"] if exc.errors() else "Validation error"
    return JSONResponse(
        status_code=422,
        content={
            "status": False,
            "message": error_msg
        }
    )

class Address(BaseModel):

    state : str
    city : str
    pincode : str

class Patient(BaseModel):

    name : Annotated[str,Field(...,description="Name of the patients")]
    age : Annotated[int, Field(...,gt=0, lt=120,description="Age must me greater then 0 and less then 121")]
    gender : Annotated[str,Literal['male','female','others'],Field(...,description="Gendor of the patients")]
    blood_group : str
    disease : Annotated[str,Field(...,description="Please enter desease of the patients")]
    phone : Annotated[str,Field(...,description="Please enter phone number of patients")]
    address : Annotated[Address,Field(...,description="Please enter address for patients")]
    height : Annotated[float,Field(...,description="Please enter height of patient")]
    weight : Annotated[float,Field(...,description="Please enter weight of the patient")]


    @field_validator('blood_group')
    def validate_blood_group(cls,value):
        valid = {'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'}
        value = value.upper()
        if value not in valid :
            raise ValueError(f"Invalid blood group. Allowed values are: {', '.join(valid)}")
        return value
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2),2)
        return bmi
    

    @computed_field
    @property
    def verdict(self)-> str:
        if(self.bmi < 20):
            return "Underweight"
        elif(self.bmi < 35):
            return "Normal"
        else:
            return "Overweight"
    


def generate_id(patients):
    if not patients:
        return 1
    return max(p['id'] for p in patients) +1


def get_patient():
    with open(file_name,"r") as f :
        data = json.load(f)
    return data    

def save_data(data):
    with open(file_name,'w') as f:
        json.dump(data,f, indent=4)


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


@app.get("/sort_patients")
def get_patients(gender: str = Query(None,description="male or female"),
                 order: str = Query('asc',description="asc or desc")):
    data = get_patient();
    patients = data["patients"]

    if gender :
        if gender.lower() not in ['male','female']:
            HTTPException(status_code= 400,detail="Gender must be male or female")

        patients = [p for p in patients if(p["gender"].lower() == gender.lower())]   


    if order not in ['asc',"desc"]:
        HTTPException(status_code=400,detail="Order must be asc or desc")

    reverse = True if order == 'desc' else False

    patients = sorted(
        patients,
        key=lambda x : x['age'],
        reverse=reverse
    )

    return {
        "status" : True,
        'count' : len(patients),
        'patients' : patients
    }




@app.post('/create_user')
def create_patients(patient : Patient):

    data = get_patient()
    patients = data['patients']

    # ✅ generate unique id
    new_id = generate_id(patients)

    # convert pydantic model to dict
    patient_dict = patient.model_dump()

    # add id
    patient_dict['id'] = new_id

    patients.append(patient_dict)
    
    data['patients'] = patients
    
    save_data(data)

    return JSONResponse(status_code = 200,        
            content={
            "message": "Patient added successfully",
            "id": new_id
        }
)



    
