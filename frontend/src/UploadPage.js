import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Container, Row, Col, Button, Form, Image, Spinner } from "react-bootstrap";

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || "https://leaf-disease-production.up.railway.app";

function UploadPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);  // Changed from "image" to "file"

    try {
      setLoading(true);
      console.log("Sending request to:", `${API_BASE_URL}/predict`);
      
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      console.log("Response status:", response.status);
      console.log("Response headers:", [...response.headers.entries()]);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Response data:", data);
      
      if (data.success) {
        // Transform the prediction data for the chart
        const predictions = data.prediction;
        console.log("Predictions object:", predictions);
        
        const chartData = Object.entries(predictions.all_predictions)
          .sort(([,a], [,b]) => b - a) // Sort by confidence descending
          .slice(0, 5) // Take top 5
          .map(([name, probability]) => ({
            name: name.replace(/___/g, ' - ').replace(/_/g, ' '), // Clean up class names
            probability: probability
          }));
        
        console.log("Chart data:", chartData);
        
        // navigate to result page with predictions and preview
        navigate("/result", { 
          state: { 
            predictions: chartData, 
            preview,
            topPrediction: {
              class: predictions.predicted_class.replace(/___/g, ' - ').replace(/_/g, ' '),
              confidence: predictions.confidence
            }
          } 
        });
      } else {
        console.error("Prediction failed:", data.error);
        alert("Prediction failed: " + (data.error || "Unknown error"));
      }
    } catch (error) {
      console.error("Upload error:", error);
      alert("Upload failed: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="py-5">
      <Row>
        <Col md={6}>
          <Form.Group controlId="formFile" className="mb-3">
            <Form.Label>Upload Leaf Image</Form.Label>
            <Form.Control type="file" accept="image/*" onChange={handleFileChange} />
          </Form.Group>
          {preview && <Image src={preview} fluid className="mb-3" />}
          <Button
            type="button"
            variant="success"
            disabled={!selectedFile || loading}
            onClick={handleUpload}
            className="w-100"
          >
            {loading ? "Predicting..." : "Detect Disease"}
          </Button>
        </Col>
      </Row>
    </Container>
  );
}

export default UploadPage;
