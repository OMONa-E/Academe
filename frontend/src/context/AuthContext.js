import React, { createContext, useState, useEffect } from 'react';
import { getAccessToken, logout as logoutService } from '../services/authService';
import { jwtDecode } from "jwt-decode";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = getAccessToken();
    if (token) {
      const decodedToken = jwtDecode(token);
      setUser({ ...decodedToken, token });
    }
  }, []);

  const isAuthenticated = () => !!user;
  const getUserRole = () => user ? user.role : null;

  const handleLogout = () => {
    logoutService();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, getUserRole, setUser, handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
};
