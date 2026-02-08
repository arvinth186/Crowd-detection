<h1>🚨 Crowd Anomaly Detection System</h1>

<p>
An end-to-end <b>AI-powered Crowd Anomaly Detection application</b> that detects abnormal crowd motion
using <b>optical flow</b> from consecutive images.
The project consists of a <b>FastAPI backend</b> and a <b>React (Vite + TypeScript) frontend</b>,
fully deployed using <b>Render</b>.
</p>

<hr/>

<h2>📌 Key Concept</h2>
<p>
This system works on <b>motion-based anomaly detection</b>.
Unlike single-image classifiers, it requires
<b>at least two consecutive images from the same scene</b> to detect abnormal motion.
</p>

<ul>
  <li>The <b>first image</b> initializes the scene</li>
  <li>The <b>next image(s)</b> are compared using optical flow</li>
  <li>High motion deviation → <b>Anomaly</b></li>
</ul>

<hr/>

<h2>🧠 How It Works</h2>

<ol>
  <li>User uploads <b>multiple consecutive images</b> from the same camera/scene</li>
  <li>Backend computes <b>optical flow (Farneback)</b> between frames</li>
  <li>Average motion magnitude is calculated</li>
  <li>Motion score is compared against a learned <b>threshold</b></li>
  <li>Status returned as <b>WAITING / NORMAL / ANOMALY</b></li>
</ol>

<hr/>

<h2>🗂 Project Structure</h2>

<pre>
Crowd-detection/
│
├── backend/
│   ├── app.py                 # FastAPI backend
│   ├── requirements.txt       # Python dependencies
│   └── trained_model.json     # Learned motion threshold
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # React UI logic
│   │   ├── App.css            # Styling
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
│
├── Notebook/
│   └── play_ucsd_frames.ipynb # Dataset exploration
│
└── README.md
</pre>

<hr/>

<h2>⚙️ Backend (FastAPI)</h2>

<h3>🔹 Tech Stack</h3>
<ul>
  <li>FastAPI</li>
  <li>OpenCV</li>
  <li>NumPy</li>
  <li>Python</li>
</ul>

<h3>🔹 API Endpoint</h3>

<pre>
POST /detect
</pre>

<p><b>Request:</b> multipart/form-data</p>

<pre>
file: image
X-Session-ID: unique-session-id
</pre>

<p><b>Response:</b></p>

<pre>
{
  "status": "WAITING | NORMAL | ANOMALY",
  "motion_score": 0.2211,
  "threshold": 0.3433,
  "message": "No anomaly detected"
}
</pre>

<p>
<b>Note:</b> The backend maintains session-based frame comparison,
so the first frame always returns <code>WAITING</code>.
</p>

<hr/>

<h2>🎨 Frontend (React + TypeScript)</h2>

<h3>🔹 Tech Stack</h3>
<ul>
  <li>React</li>
  <li>TypeScript</li>
  <li>Vite</li>
  <li>Axios</li>
</ul>

<h3>🔹 Features</h3>
<ul>
  <li>Multiple image upload</li>
  <li>Session-based detection</li>
  <li>Clear WAITING / NORMAL / ANOMALY states</li>
  <li>Info tooltip explaining 2-image requirement</li>
  <li>Clean card-based UI</li>
</ul>

<p>
ℹ️ An info icon is provided in the UI to explain why
<b>more than one image is required</b>.
</p>

<hr/>

<h2>🚀 Deployment</h2>

<h3>Backend</h3>
<ul>
  <li>Deployed as a <b>Web Service</b> on Render</li>
  <li>Runs FastAPI with Uvicorn</li>
</ul>

<h3>Frontend</h3>
<ul>
  <li>Deployed as a <b>Static Site</b> on Render</li>
  <li>Built using <code>npm run build</code></li>
  <li>Published from <code>dist/</code> directory</li>
</ul>

<hr/>

<h2>⚠️ Important Notes</h2>

<ul>
  <li>This system <b>will not work correctly with a single image</b></li>
  <li>Images must be <b>consecutive frames</b> from the same scene</li>
  <li>Refreshing the page resets the detection session</li>
</ul>

<hr/>

<h2>📈 Future Improvements</h2>

<ul>
  <li>Video upload support</li>
  <li>Real-time webcam integration</li>
  <li>Heatmap visualization</li>
  <li>Persistent session storage</li>
  <li>Alert notifications</li>
</ul>

<hr/>

<h2>👨‍💻 Author</h2>

<p>
<b>Arvinth Athikesav</b><br/>
AI / ML Developer<br/>
</p>

<p>
Built as part of an applied AI/ML project focusing on
<b>computer vision and real-world anomaly detection</b>.
</p>
