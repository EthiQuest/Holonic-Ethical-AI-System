import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const PerformanceMetrics = () => {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    // In a real application, you would fetch this data from your backend
    const fetchMetrics = async () => {
      // Simulating API call with mock data
      const mockData = [
        { timestamp: '00:00', systemPerformance: 85, taskCompletion: 78, ethicalAlignment: 92 },
        { timestamp: '04:00', systemPerformance: 88, taskCompletion: 82, ethicalAlignment: 94 },
        { timestamp: '08:00', systemPerformance: 92, taskCompletion: 88, ethicalAlignment: 95 },
        { timestamp: '12:00', systemPerformance: 90, taskCompletion: 85, ethicalAlignment: 93 },
        { timestamp: '16:00', systemPerformance: 87, taskCompletion: 80, ethicalAlignment: 91 },
        { timestamp: '20:00', systemPerformance: 89, taskCompletion: 84, ethicalAlignment: 92 },
      ];
      setMetrics(mockData);
    };

    fetchMetrics();
  }, []);

  return (
    <div>
      <h2>Performance Metrics</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={metrics}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="systemPerformance" stroke="#8884d8" name="System Performance" />
          <Line type="monotone" dataKey="taskCompletion" stroke="#82ca9d" name="Task Completion" />
          <Line type="monotone" dataKey="ethicalAlignment" stroke="#ffc658" name="Ethical Alignment" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PerformanceMetrics;