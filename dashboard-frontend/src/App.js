import React, { useState, useEffect } from 'react';
import StrategicDirectives from './components/StrategicDirectives';
import AgentCommunication from './components/AgentCommunication';
import AgentList from './components/AgentList';
import SystemMonitor from './components/SystemMonitor';
import PerformanceMetrics from './components/PerformanceMetrics';
import { getAgentList } from './services/api';
import './App.css'; // We'll create this file for styling

function App() {
  const [agents, setAgents] = useState([]);
  const [activeTab, setActiveTab] = useState('directives');

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    const data = await getAgentList();
    setAgents(data.agents);
  };

  const renderActiveComponent = () => {
    switch(activeTab) {
      case 'directives':
        return <StrategicDirectives />;
      case 'communication':
        return <AgentCommunication agents={agents} />;
      case 'agents':
        return <AgentList />;
      case 'monitor':
        return <SystemMonitor />;
      case 'metrics':
        return <PerformanceMetrics />;
      default:
        return <StrategicDirectives />;
    }
  };

  return (
    <div className="App">
      <h1 className="app-title">Holonic AI Swarm</h1>
      <div className="tab-container">
        <button className={`tab ${activeTab === 'directives' ? 'active' : ''}`} onClick={() => setActiveTab('directives')}>Directives</button>
        <button className={`tab ${activeTab === 'communication' ? 'active' : ''}`} onClick={() => setActiveTab('communication')}>Communicate</button>
        <button className={`tab ${activeTab === 'agents' ? 'active' : ''}`} onClick={() => setActiveTab('agents')}>Agents</button>
        <button className={`tab ${activeTab === 'monitor' ? 'active' : ''}`} onClick={() => setActiveTab('monitor')}>Monitor</button>
        <button className={`tab ${activeTab === 'metrics' ? 'active' : ''}`} onClick={() => setActiveTab('metrics')}>Metrics</button>
      </div>
      <div className="content-container">
        {renderActiveComponent()}
      </div>
    </div>
  );
}

export default App;