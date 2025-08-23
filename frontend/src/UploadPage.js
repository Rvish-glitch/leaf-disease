import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Container, Row, Col, Button, Form, Image, Spinner } from "react-bootstrap";

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
    formData.append("image", selectedFile);

    try {
      setLoading(true);
      await fetch("http://localhost:5000/predict", {
        method: "POST",
        body: formData,
      });

      await new Promise((res) => setTimeout(res, 1500)); // wait for file to be written
      const res = await fetch("/predictions.json");
      const data = await res.json();

      // navigate to result page with predictions and preview
      navigate("/result", { state: { predictions: data.predictions, preview } });
    } catch (error) {
      console.error("Upload error:", error);
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
