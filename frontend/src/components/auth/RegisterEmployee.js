import React, { useState } from 'react';
import { registerEmployee } from '../../services/authService';

function RegisterEmployee({ onRegister }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await registerEmployee({ username, email, password });
      onRegister();
    } catch (error) {
      console.error("Error registering employee:", error);
    }
  };

  return (
    <form onSubmit={handleRegister}>
      <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
      <button type="submit">Register Employee</button>
    </form>
  );
}

export default RegisterEmployee;
