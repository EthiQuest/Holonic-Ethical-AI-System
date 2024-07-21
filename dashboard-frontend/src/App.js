import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from 'recharts';
import { Button, Select, MenuItem, FormControl, InputLabel, Typography, Grid, Paper } from '@material-ui/core';
import ForceGraph2D from 'react-force-graph-2d';

const socket = io('http://localhost:5000');

function App() {
  const [systemData, setSystemData] = useState(null);
  const [performanceHistory, setPerformanceHistory] = useState([]);
  const [holonPerformanceHistory, setHolonPerformanceHistory] = useState({});
  const [holonNetwork, setHolonNetwork] = useState({ nodes: [], links: [] });

  useEffect(() => {
    socket.on('system_update', (data) => {
      setSystemData(data);
      setPerformanceHistory(prev => [...prev, { cycle: data.current_cycle, performance: data.performance }]);
      
      // Update holon performance history
      const newHolonPerformance = {};
      Object.entries(data.holon_performance).forEach(([holonName, performance]) => {
        newHolonPerformance[holonName] = [
          ...(holonPerformanceHistory[holonName] || []),
          { cycle: data.current_cycle, ...performance }
        ];
      });
      setHolonPerformanceHistory(newHolonPerformance);

      // Update holon network
      setHolonNetwork(data.holon_network);
    });

    // Fetch initial holon performance history
    fetch('http://localhost:5000/holon_performance_history')
      .then(response => response.json())
      .then(data => setHolonPerformanceHistory(data));

    // Fetch initial holon network
    fetch('http://localhost:5000/holon_network')
      .then(response => response.json())
      .then(data => setHolonNetwork(data));

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
        {/* Existing components... */}
    
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

        {/* Holon Network Graph */}
        <Grid item xs={12}>
          <Paper style={{ padding: 16 }}>
            <Typography variant="h6">Holon Hierarchy</Typography>
            <div style={{ height: '400px' }}>
              <ForceGraph2D
                graphData={holonNetwork}
                nodeLabel="name"
                nodeAutoColorBy="capabilities"
                linkDirectionalArrowLength={3.5}
                linkDirectionalArrowRelPos={1}
                linkCurvature={0.25}
              />
            </div>
          </Paper>
        </Grid>

        {/* Holon Performance Charts */}
        {systemData.holons.map(holon => (
          <Grid item xs={12} md={6} key={holon.id}>
            <Paper style={{ padding: 16 }}>
              <Typography variant="h6">{holon.name} Performance</Typography>
              <LineChart width={500} height={300} data={holonPerformanceHistory[holon.name]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="cycle" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="success_rate" stroke="#8884d8" name="Success Rate" />
                <Line type="monotone" dataKey="resource_utilization" stroke="#82ca9d" name="Resource Utilization" />
              </LineChart>
              <BarChart width={500} height={300} data={[systemData.holon_performance[holon.name]]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="tasks_completed" fill="#8884d8" name="Tasks Completed" />
                <Bar dataKey="avg_completion_time" fill="#82ca9d" name="Avg Completion Time" />
              </BarChart>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </div>
  );
}

export default App;