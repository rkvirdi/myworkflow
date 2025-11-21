# from fastapi import FastAPI , Path, HTTPException, Query
# from helpers import load_data

# data = load_data()

# app = FastAPI()


from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
import time
import json

app = FastAPI()

# ---------------------------
# Patient Data (In-memory DB)
# ---------------------------
patients = [
    {
        "patient_id": "P001",
        "name": "John Doe",
        "age": 45,
        "gender": "Male",
        "phone": "555-123-4567",
        "address": "123 Elm Street, Sacramento, CA",
        "primary_doctor": "Dr. Emily Smith"
    },
    {
        "patient_id": "P002",
        "name": "Maria Lopez",
        "age": 32,
        "gender": "Female",
        "phone": "555-987-6543",
        "address": "89 Pine Avenue, Elk Grove, CA",
        "primary_doctor": "Dr. Andrew Chen"
    },
    {
        "patient_id": "P003",
        "name": "Sam Patel",
        "age": 29,
        "gender": "Male",
        "phone": "555-444-8888",
        "address": "45 Oak Drive, Folsom, CA",
        "primary_doctor": "Dr. Olivia Martinez"
    },
    {
        "patient_id": "P004",
        "name": "Aisha Brown",
        "age": 67,
        "gender": "Female",
        "phone": "555-222-3333",
        "address": "200 River Blvd, Roseville, CA",
        "primary_doctor": "Dr. Jack Reynolds"
    }
]

# ---------------------------
# Health endpoint
# ---------------------------

'''Method: GET
Purpose: To verify that the service is running.

What it does:

Returns a simple JSON response confirming the API is alive.

Used by load balancers, monitoring tools, or Kubernetes liveness probes.'''


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Service is healthy"}

# ---------------------------
# GET endpoint (Read patient)
# ---------------------------

'''Method: GET
Purpose: Retrieve a single patient’s information using their ID.

What it does:

Searches the in-memory patient database.

If the patient exists → returns full patient details.

If not → returns a 404 "Patient not found".

Example Use Case:
A doctor’s dashboard needs to pull a patient profile.'''

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    for p in patients:
        if p["patient_id"] == patient_id:
            return p
    raise HTTPException(status_code=404, detail="Patient not found")

# ---------------------------
# POST endpoint (Create patient)
# ---------------------------

'''Method: POST
Purpose: Add a new patient record into the system.

What it does:

Accepts a patient JSON body.

Appends it to the existing patient list.

Returns a message + updated count of total patients.

Example Use Case:
A receptionist enters a new patient into the system.'''

@app.post("/patients")
def create_patient(payload: dict):
    patients.append(payload)
    return {"message": "Patient added", "count": len(patients)}

# ---------------------------
# PUT endpoint (Update patient)
# ---------------------------

'''Method: PUT
Purpose: Update a patient’s existing data.

What it does:

Looks up the patient by ID.

Updates the fields provided in the request body.

Returns updated patient data.

If ID not found → returns 404.

Example Use Case:
Changing a patient's phone number or address after they submit an update form.'''

@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, payload: dict):
    for index, p in enumerate(patients):
        if p["patient_id"] == patient_id:
            patients[index].update(payload)
            return {"message": "Patient updated", "data": patients[index]}
    raise HTTPException(status_code=404, detail="Patient not found")

# ---------------------------
# STREAMING endpoint
# ---------------------------

'''Method: GET
Purpose: Demonstrates server streaming data continuously.

What it does:

Sends data in chunks (one line at a time).

Useful for sending long-running task updates (e.g., file processing).

How it works:

Function yields one line every second.

Browser or client sees data arriving progressively.

Real Use Cases:

Real-time logs

Video/audio streams

Large dataset streaming'''

def generate_stream():
    for i in range(1, 6):
        time.sleep(1)
        yield f"Processing chunk {i}\n"

@app.get("/stream")
def stream_data():
    return StreamingResponse(generate_stream(), media_type="text/plain")

# ---------------------------
# Server-sent events SSE endpoint
# ---------------------------

'''Method: GET
Purpose: Push live events to the client over a single long-lived connection.

What it does:

Sends JSON events one by one every second.

Client does NOT need to poll — server pushes updates automatically.



Real Use Cases:

Live notifications

Dashboard updates

Chat messages

Realtime status indicators'''

async def event_generator():
    for i in range(5):
        await asyncio.sleep(1)
        yield {"data": json.dumps({"event_number": i})}

@app.get("/sse")
async def sse_endpoint():
    return EventSourceResponse(event_generator())
