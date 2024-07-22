import React, { useState, useEffect } from 'react';
import { getAgentList } from '../services/api';

const AgentList = () => {
  const [agents, setAgents] = useState([]);

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    const data = await getAgentList();
    setAgents(data.agents);
  };

  return (
    <div>
      <h2>Agent List</h2>
      <ul>
        {agents.map((agent) => (
          <li key={agent.id}>{agent.name} - {agent.role}</li>
        ))}
      </ul>
    </div>
  );
};

export default AgentList;