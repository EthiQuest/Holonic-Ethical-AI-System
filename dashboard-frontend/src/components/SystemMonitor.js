import React, { useState, useEffect } from 'react';

const SystemMonitor = () => {
  const [systemStatus, setSystemStatus] = useState({
    activeAgents: 0,
    tasksPending: 0,
    tasksCompleted: 0,
    systemHealth: 'Unknown'
  });

  useEffect(() => {
    // In a real application, you would fetch this data from your backend
    const fetchSystemStatus = async () => {
      // Simulating API call with mock data
      const mockStatus = {
        activeAgents: 15,
        tasksPending: 27,
        tasksCompleted: 143,
        systemHealth: 'Good'
      };
      setSystemStatus(mockStatus);
    };

    fetchSystemStatus();
    // Set up an interval to fetch status regularly
    const intervalId = setInterval(fetchSystemStatus, 60000); // every minute

    // Clean up interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      <h2>System Monitor</h2>
      <div>
        <p>Active Agents: {systemStatus.activeAgents}</p>
        <p>Tasks Pending: {systemStatus.tasksPending}</p>
        <p>Tasks Completed: {systemStatus.tasksCompleted}</p>
        <p>System Health: {systemStatus.systemHealth}</p>
      </div>
    </div>
  );
};

export default SystemMonitor;