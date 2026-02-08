from fastapi import FastAPI,File,UploadFile
import cv2
import numpy as np
import json
import tempfile
import os

app = FastAPI(title="Crowd Detection API")

with open("trained_model.json","r") as f:
    model = json.load(f)

THRESHOLD = model['threshold']

last_frame = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Crowd Detection API"}

@app.post("/detect")
async def detect_crowd_anomaly(file: UploadFile = File(...)):
    global last_frame

    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    frame = cv2.imread(tmp_path)
    os.remove(tmp_path)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # First frame → no detection
    if last_frame is None:
        last_frame = gray
        return {
            "status": "WAITING",
            "message": "Need one more frame to compute motion"
        }

    # Optical flow
    flow = cv2.calcOpticalFlowFarneback(
        last_frame, gray,
        None,
        0.5, 3, 15, 3, 5, 1.2, 0
    )

    magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    motion_score = float(np.mean(magnitude))

    last_frame = gray

    if motion_score > THRESHOLD:
        status = "ANOMALY"
    else:
        status = "NORMAL"

    return {
        "status": status,
        "motion_score": round(motion_score, 4),
        "threshold": THRESHOLD,
        "message": "Anomaly detected" if status == "ANOMALY" else "No anomaly detected"
    }
