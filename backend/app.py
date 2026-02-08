from fastapi import FastAPI, File, UploadFile, Header
from fastapi.middleware.cors import CORSMiddleware

import cv2
import numpy as np
import json
import tempfile
import os

app = FastAPI(title="Crowd Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained threshold
with open("trained_model.json", "r") as f:
    model = json.load(f)

THRESHOLD = model["threshold"]

# ✅ Store last frame PER SESSION
last_frames = {}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Crowd Detection API"}

@app.post("/detect")
async def detect_crowd_anomaly(
    file: UploadFile = File(...),
    x_session_id: str = Header(...)
):
    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    frame = cv2.imread(tmp_path)
    os.remove(tmp_path)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 🟡 First frame for this session
    if x_session_id not in last_frames:
        last_frames[x_session_id] = gray
        return {
            "status": "WAITING",
            "message": "First frame received. Upload next image from same scene."
        }

    # Optical flow between consecutive frames
    prev_gray = last_frames[x_session_id]

    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, gray,
        None,
        0.5, 3, 15, 3, 5, 1.2, 0
    )

    magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    motion_score = float(np.mean(magnitude))

    # Update last frame
    last_frames[x_session_id] = gray

    status = "ANOMALY" if motion_score > THRESHOLD else "NORMAL"

    return {
        "status": status,
        "motion_score": round(motion_score, 4),
        "threshold": THRESHOLD,
        "message": "Anomaly detected" if status == "ANOMALY" else "No anomaly detected"
    }
