import React, { useState } from "react";
import { Container, Row, Col, Button, Form, Image, Spinner } from "react-bootstrap";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    if (file) {
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleUpload = async (e) => {
    // Prevent default form submission behavior
    e.preventDefault();
    
    if (!selectedFile) return;
    
    const formData = new FormData();
    formData.append("image", selectedFile); 
    
    try {
      setLoading(true);
      setPredictions([]);
      const response = await fetch(`${process.env.REACT_APP_API_URL || "http://localhost:5000"}/predict`, {
        method: "POST",
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error("Failed to get prediction");
      }
      const data = await response.json();
      setPredictions(data.predictions || []);
    } catch (error) {
      console.error("Prediction error:", error);
      alert("Error getting predictions. Please try again.");
    } finally {
      setLoading(false);
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
