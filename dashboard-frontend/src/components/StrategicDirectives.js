import React, { useState, useEffect } from 'react';
import { getStrategicDirectives, setStrategicDirectives } from '../services/api';
import './StrategicDirectives.css';

const StrategicDirectives = () => {
  const [directives, setDirectives] = useState({ vision: '', mission: '', okrs: [] });

  useEffect(() => {
    fetchDirectives();
  }, []);

  const fetchDirectives = async () => {
    const data = await getStrategicDirectives();
    setDirectives(data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await setStrategicDirectives(directives);
    alert('Strategic directives updated successfully');
  };

  return (
    <div className="strategic-directives">
      <h2>Strategic Directives</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="vision">Vision:</label>
          <input
            id="vision"
            type="text"
            value={directives.vision}
            onChange={(e) => setDirectives({ ...directives, vision: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label htmlFor="mission">Mission:</label>
          <input
            id="mission"
            type="text"
            value={directives.mission}
            onChange={(e) => setDirectives({ ...directives, mission: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label htmlFor="okrs">OKRs:</label>
          <textarea
            id="okrs"
            value={directives.okrs.join('\n')}
            onChange={(e) => setDirectives({ ...directives, okrs: e.target.value.split('\n') })}
          />
        </div>
        <button type="submit" className="submit-btn">Update Directives</button>
      </form>
    </div>
  );
};

export default StrategicDirectives;