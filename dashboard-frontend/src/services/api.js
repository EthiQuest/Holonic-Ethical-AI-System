import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const getStrategicDirectives = async () => {
  const response = await axios.get(`${API_URL}/strategic_directives`);
  return response.data;
};

export const setStrategicDirectives = async (directives) => {
  const response = await axios.post(`${API_URL}/strategic_directives`, directives);
  return response.data;
};

export const sendMessage = async (recipient, message) => {
  const response = await axios.post(`${API_URL}/communicate`, { recipient, message });
  return response.data;
};

export const getAgentList = async () => {
  const response = await axios.get(`${API_URL}/agents`);
  return response.data;
};

// Add other API calls as needed