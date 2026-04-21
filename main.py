import uvicorn
from fastapi import FastAPI, HTTPException, Query
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


# @app.get("/sort")
# def sort_patient(gender: str = Query(None, description="male or female"),
    #     order: str = Query("asc", description="asc or desc (age sorting)")):
    
    # valid_fields = ["id", "name", "age", "gender", "blood_group"]
    # valid_order = ["asc", "desc"]

    # if gender not in valid_fields :
    #     raise HTTPException(status_code=400,detail= f"Invalid fields selected from {valid_fields}")
    #     # return {"status": False,"message" : "Invalid fields selected from {valid_fields}"}


    
    # if order not in  valid_order :
    #     raise HTTPException(status_code=400,detail= f"Invalid fields selected from {valid_order}")
    
    # data = get_patient()

    # reverse = True if order == 'decs' else False

    # sorted_data = sorted(data['patients'],key=lambda x : str(x.get(gender,0).lower()),reverse= reverse)

    # if(sorted_data != ""):
    #     return {'status' : True,'sorted_data':sorted_data}
    # else :
    #     return {'status' : False, 'sorted_data' : sorted_data}
    


# @app.get("/patients")
# def get_patients(
#     gender: str = Query(None, description="male or female"),
#     order: str = Query("asc", description="asc or desc (age sorting)")
# ):
#     data = get_patient()
#     patients = data["patients"]

#     # ✅ Filter by gender
#     if gender:
#         if gender.lower() not in ["male", "female"]:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Gender must be 'male' or 'female'"
#             )
#         patients = [
#             p for p in patients
#             if p["gender"].lower() == gender.lower()
#         ]

#     # ✅ Sort by age
#     if order not in ["asc", "desc"]:
#         raise HTTPException(
#             status_code=400,
#             detail="Order must be 'asc' or 'desc'"
#         )

#     reverse = True if order == "desc" else False

#     patients = sorted(
#         patients,
#         key=lambda x: x["age"],
#         reverse=reverse
#     )

#     return {
#         "status": True,
#         "count": len(patients),
#         "data": patients
#     }


@app.get("/sort_patients")
def get_patients(gender: str = Query(None,description="male or female"),
                 order: str = Query('asc',description="asc or desc")):
    data = get_patient();
    patients = data["patients"]

    if gender :
        if gender.lower() not in ['male','female']:
            HTTPException(status_code= 400,detail="Gender must be male or female")
        patients = [
            p for p in patients
            if(p["gender"].lower() == gender.lower())
        ]   

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