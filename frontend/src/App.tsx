import { useState, useRef } from "react";
import axios from "axios";
import "./App.css";

interface ApiResponse {
  status: string;
  motion_score?: number;
  threshold?: number;
  message: string;
}

const API_URL = "https://crowd-detection-x621.onrender.com/detect";

function App() {
  const [files, setFiles] = useState<File[]>([]);
  const [results, setResults] = useState<ApiResponse[]>([]);
  const [loading, setLoading] = useState(false);

  // One session per page load
  const sessionIdRef = useRef<string>(crypto.randomUUID());

  const handleUpload = async () => {
    if (files.length < 2) {
      alert("Please upload at least TWO images from the same scene.");
      return;
    }

    setResults([]);
    setLoading(true);

    try {
      for (const file of files) {
        const formData = new FormData();
        formData.append("file", file);

        const response = await axios.post<ApiResponse>(
          API_URL,
          formData,
          {
            headers: {
              "X-Session-ID": sessionIdRef.current,
            },
          }
        );

        setResults((prev) => [...prev, response.data]);
      }
    } catch (err) {
      console.error(err);
      alert("Failed to connect to API");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="card">

        {/* Info Icon */}
        <div className="info-container">
          <span className="info-icon">ⓘ</span>
          <div className="info-tooltip">
            Motion-based detection requires at least <b>two consecutive images</b>.
            <br />
            The first image initializes the scene, and the next images are used to
            detect anomalies.
          </div>
        </div>

        <h1>🚨 Crowd Anomaly Detection</h1>

        <p className="subtitle">
          Upload <strong>at least 2 consecutive images</strong> from the same scene
        </p>

        <input
          type="file"
          accept="image/*"
          multiple
          onChange={(e) =>
            setFiles(e.target.files ? Array.from(e.target.files) : [])
          }
        />

        <button onClick={handleUpload} disabled={loading}>
          {loading ? "Processing..." : "Upload Images"}
        </button>

        {/* RESULTS */}
        {results.map((result, index) => (
          <div
            key={index}
            className={`result ${
              result.status === "ANOMALY" ? "anomaly" : "normal"
            }`}
          >
            <p>
              <strong>Frame {index + 1}:</strong> {result.status}
            </p>

            {result.status === "WAITING" ? (
                <p style={{ fontStyle: "italic", color: "#065f46" }}>
                    Baseline frame initialized (used for motion comparison)
                </p>
            ) : (
              <>
                <p><strong>Motion Score:</strong> {result.motion_score}</p>
                <p><strong>Threshold:</strong> {result.threshold}</p>
                <p><strong>Message:</strong> {result.message}</p>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
