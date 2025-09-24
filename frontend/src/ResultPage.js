import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Container, Row, Col, Image, Button } from "react-bootstrap";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid
} from "recharts";

function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { predictions, preview, topPrediction } = location.state || {};

  if (!predictions || !preview) {
    return (
      <Container className="py-5 text-center">
        <p>No prediction data found.</p>
        <Button onClick={() => navigate("/")}>Go Back</Button>
      </Container>
    );
  }

  return (
    <Container className="py-5">
      <Row>
        <Col md={5}>
          <Image src={preview} fluid rounded />
          {topPrediction && (
            <div className="mt-3 p-3 bg-light rounded">
              <h5 className="text-success mb-2">Top Prediction</h5>
              <p className="mb-1"><strong>{topPrediction.class}</strong></p>
              <p className="mb-0 text-muted">Confidence: {(topPrediction.confidence * 100).toFixed(2)}%</p>
            </div>
          )}
        </Col>
        <Col md={7}>
          <h3 className="mb-4 text-success text-center">Top 5 Predictions</h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={predictions}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 1]} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
              <Tooltip formatter={(v) => `${(v * 100).toFixed(2)}%`} />
              <Bar dataKey="probability" fill="#198754" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="text-center mt-3">
            <Button onClick={() => navigate("/")}>Upload Another</Button>
          </div>
        </Col>
      </Row>
    </Container>
  );
}

export default ResultPage;
