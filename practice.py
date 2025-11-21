
# @app.get("/health")
# def health_check():
#     return {"status": "ok", "message": "Service is healthy"}

# @app.get("/")
# def root():
#     return {"message": "Welcome to the Patients Data API"}

# @app.get("/patients")
# def get_patients():
    
#     return {"patients_data": data}

# #path parameter example

# @app.get("/patients/{patient_id}")
# def get_patient_by_id(patient_id: str = Path(..., description="The ID of the patient to retrieve",example="P001")):
   
#     for patient in data:
#         if patient["patient_id"] == patient_id:
#             return {"patient_data": patient}
#     raise HTTPException(status_code=404, detail="Patient not found")

# #query parameter example

# @app.get("/sort_patients")
# def sort_patients_by_age(sort_by: str = Query(..., description="Sort patient on the basis of age or name"), 
#                          order:str = Query('asc',description="Order of sorting, asc or desc")):
#    valid_fields = ['age', 'name']
#    if sort_by not in valid_fields:
#          raise HTTPException(status_code=400, detail=f"Invalid sort_by field. Must be one of {valid_fields}")
   
#    if order not in ['asc', 'desc']:
#          raise HTTPException(status_code=400, detail="Invalid order. Must be 'asc' or 'desc'")
   
#    sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=(order=='desc'))
#    return {"sorted_patients": sorted_data}
