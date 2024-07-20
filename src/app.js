import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Button, Select, MenuItem, FormControl, InputLabel, Typography, Grid, Paper } from '@material-ui/core';

const socket = io('http://localhost:5000');

function App() {
  const [systemData, setSystemData] = useState(null);
  const [performanceHistory, setPerformanceHistory] = useState([]);

  useEffect(() => {
    socket.on('system_update', (data) => {
      setSystemData(data);
      setPerformanceHistory(prev => [...prev, { cycle: data.current_cycle, performance: data.performance }]);
    });

    return () => {
      socket.off('system_update');
    };
  }, []);

  const handleIntervention = (type, target, capability) => {
    socket.emit('intervene', { type, target, capability });
  };

  if (!systemData) return <div>Loading...</div>;

  return (
    <div className="App">
      <Typography variant="h4" gutterBottom>Holonic System Dashboard</Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper style={{ padding: 16 }}>
            <Typography variant="h6">System Overview</Typography>
            <p>Current Scenario: {systemData.current_scenario}</p>
            <p>Current Cycle: {systemData.current_cycle}</p>
            <p>Overall Performance: {systemData.performance.toFixed(2)}</p>
            <Button variant="contained" color="primary" onClick={() => handleIntervention('trigger_restructuring')}>
              Trigger Restructuring
            </Button>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper style={{ padding: 16 }}>
            <Typography variant="h6">Active Events</Typography>
            <ul>
              {systemData.active_events.map((event, index) => (
                <li key={index}>{event}</li>
              ))}
            </ul>
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper style={{ padding: 16 }}>
            <Typography variant="h6">Performance History</Typography>
            <LineChart width={600} height={300} data={performanceHistory}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="cycle" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="performance" stroke="#8884d8" />
            </LineChart>
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper style={{ padding: 16 }}>
            <Typography variant="h6">Holons</Typography>
            {systemData.holons.map(holon => (
              <div key={holon.id} style={{ marginBottom: 16 }}>
                <Typography variant="subtitle1">{holon.name}</Typography>
                <p>Capabilities: {holon.capabilities.join(', ')}</p>
                <p>Operational: {holon.operational ? 'Yes' : 'No'}</p>
                <p>Pending Tasks: {holon.pending_tasks.join(', ')}</p>
                <FormControl>
                  <InputLabel>Add Capability</InputLabel>
                  <Select
                    onChange={(e) => handleIntervention('add_capability', holon.name, e.target.value)}
                  >
                    <MenuItem value="data_processing">Data Processing</MenuItem>
                    <MenuItem value="decision_making">Decision Making</MenuItem>
                    <MenuItem value="resource_management">Resource Management</MenuItem>
                  </Select>
                </FormControl>
                <FormControl>
                  <InputLabel>Remove Capability</InputLabel>
                  <Select
                    onChange={(e) => handleIntervention('remove_capability', holon.name, e.target.value)}
                  >
                    {holon.capabilities.map(cap => (
                      <MenuItem key={cap} value={cap}>{cap}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </div>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}

export default App;