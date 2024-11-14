import React, { useState } from 'react';
import { registerEmployer } from '../../services/authService';

function RegisterEmployer({ onRegister }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [department, setDepartment] = useState('training');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const data = {
        user : {username, email, password}, 
        department: department,
      };
      await registerEmployer(data);
      onRegister();
    } catch (error) {
      console.error("Error registering employer:", error);
    }
  };

  return (
    <form onSubmit={handleRegister}>
      <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
      <select value={department} onChange={(e) => setDepartment(e.target.value)}>
          <option value="" disabled>Select Department</option>
          <option value="training">Training</option>
          <option value="finance">Finance</option>
          <option value="farewell">Farewell</option>
      </select>
      <button type="submit">Register Employer</button>
    </form>
  );
}

export default RegisterEmployer;
