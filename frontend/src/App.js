import React, { useEffect, useState } from "react";
import { Container, Row, Col, Button, Form, Image, Spinner } from "react-bootstrap";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

// API Configuration
import { API_BASE_URL, DEFAULT_API, logApiBase } from "./config";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [apiBase, setApiBase] = useState(API_BASE_URL);

  // On mount, log API base and check backend health quickly
  useEffect(() => {
    logApiBase();
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    fetch(`${apiBase}/health`, { signal: controller.signal, mode: "cors" })
      .then(r => {
        if (!r.ok) throw new Error(`Health check failed: ${r.status}`);
        return r.json();
      })
      .then(() => {
        // Clear any stale error
        setError("");
      })
      .catch((e) => {
        // If user had pointed to localhost (common in dev) and it failed,
        // fall back automatically to Railway default
        const looksLocal = apiBase.includes("localhost") || apiBase.includes("127.0.0.1");
        if (looksLocal) {
          setApiBase(DEFAULT_API);
          setError(`Can't reach backend at ${apiBase}. Falling back to ${DEFAULT_API}. ${e.message}`);
        } else {
          setError(`Can't reach backend at ${apiBase}. ${e.message}`);
        }
        // eslint-disable-next-line no-console
        console.error("Health check error:", e);
      })
      .finally(() => clearTimeout(timeout));
  }, [apiBase]);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    if (file) {
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    
  console.log("HandleUpload called");
  console.log("Selected file:", selectedFile);
  console.log("API URL:", `${API_BASE_URL}/predict`);
    
    if (!selectedFile) {
  console.log("No file selected");
      setError("Please select a file");
      return;
    }
    
    const formData = new FormData();
    formData.append("file", selectedFile); // Changed from "image" to "file"
  console.log("FormData created with file:", selectedFile.name);
    
    try {
      setLoading(true);
      setPredictions([]);
  console.log("Sending request to:", `${API_BASE_URL}/predict`);
      
  const response = await fetch(`${apiBase}/predict`, {
        method: "POST",
        body: formData,
        mode: "cors",
      });
      
  console.log("Response status:", response.status);
  console.log("Response ok:", response.ok);
      
      if (!response.ok) {
        // Try to pull backend error message if present
        let backendMsg = "";
        try {
          const maybeJson = await response.json();
          backendMsg = maybeJson?.error || JSON.stringify(maybeJson);
        } catch (_) {}
        throw new Error(`Failed to get prediction: ${response.status} ${backendMsg}`);
      }
      
      const data = await response.json();
  console.log("Response data:", data);
      
      if (data.success && data.prediction) {
        // Transform the prediction data for the chart
        const predictionData = data.prediction;
        const chartData = Object.entries(predictionData.all_predictions)
          .sort(([,a], [,b]) => b - a) // Sort by confidence descending
          .slice(0, 5) // Take top 5
          .map(([name, probability]) => ({
            name: name.replace(/___/g, ' - ').replace(/_/g, ' '), // Clean up class names
            probability: probability
          }));
        
        setPredictions(chartData);
  setError("");
  console.log("Predictions set successfully");
      } else {
        throw new Error("Invalid response format");
      }
    } catch (error) {
  console.error("Upload error:", error);
  setError(error.message || "Unknown error during upload");
    } finally {
      setLoading(false);
  console.log("Upload process completed");
    }
  };

  return (
  <Container 
      fluid 
      className="py-4 bg-light min-vh-100" 
      style={{
        backgroundImage: "url('/bg.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <div className="d-flex justify-content-center mb-4">
  <div className="bg-white p-3 rounded shadow-sm">
    <h1 className="mb-0 text-success text-center">
      <span role="img" aria-label="plant leaf">🌿</span> Plant's Leaf Disease Analyzer
    </h1>
  </div>
</div>

      <Row className="gx-4">
        <div className="text-muted small mb-2">Using API: {apiBase}</div>
        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}
        {/* Left column - Upload */}
        <Col md={3} className="bg-white p-4 rounded shadow-sm">
          <Form onSubmit={handleUpload}>
            <Form.Group controlId="formFile" className="mb-3">
              <Form.Label>Upload Leaf Image</Form.Label>
              <Form.Control type="file" accept="image/*" onChange={handleFileChange} />
            </Form.Group>
            
            {preview && (
              <Image
                src={preview}
                alt="Leaf preview"
                fluid
                rounded
                className="mb-3 border"
                style={{ maxHeight: "300px", objectFit: "contain" }}
              />
            )}
            
            <Button
              type="submit"
              variant="success"
              disabled={!selectedFile || loading}
              className="w-100"
            >
              {loading ? (
                <>
                  <Spinner
                    as="span"
                    animation="border"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                    className="me-2"
                  />
                  Predicting...
                </>
              ) : (
                "Detect Disease"
              )}
            </Button>
          </Form>
        </Col>
        
        {/* Right column - Chart */}
        <Col md={9} className="bg-white p-4 rounded shadow-sm">
          <h3 className="text-success mb-4 text-center">Top 5 Matching Diseases</h3>
          {predictions.length > 0 ? (
            <ResponsiveContainer width="100%" height={550}>
              <BarChart
                data={predictions}
                margin={{ top: 20, right: 30, left: 20, bottom: 40 }}
              >
                <XAxis 
					dataKey="name"
					tick={{ fontWeight:"bold",fontSize: 14 }}
				/>
                <YAxis 
                  domain={[0, 1]} 
                  tickFormatter={(val) => (val * 100).toFixed(0) + "%"} 
                  tick={{ fontWeight:"bold",fontSize: 14 }}
                />
                <Tooltip formatter={(val) => (val * 100).toFixed(2) + "%"} />
                <Bar dataKey="probability" fill="#198754" radius={[10, 10, 0, 0]} barSize={120}/>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-center py-5">
              {loading ? (
                <Spinner animation="border" variant="success" />
              ) : (
                <p className="text-muted">No predictions yet. Upload an image to get started.</p>
              )}
            </div>
          )}
        </Col>
      </Row>
    </Container>
  );
}

export default App;
