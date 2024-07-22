import React, { useState } from 'react';
import { sendMessage } from '../services/api';

const AgentCommunication = ({ agents }) => {
  const [recipient, setRecipient] = useState('ceo');
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await sendMessage(recipient, message);
    setResponse(result.response);
  };

  return (
    <div>
      <h2>Communicate with Agents</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Recipient:</label>
          <select value={recipient} onChange={(e) => setRecipient(e.target.value)}>
            <option value="ceo">CEO</option>
            {agents.map((agent) => (
              <option key={agent.id} value={agent.id}>{agent.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label>Message:</label>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
        </div>
        <button type="submit">Send Message</button>
      </form>
      {response && (
        <div>
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default AgentCommunication;