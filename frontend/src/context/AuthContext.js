import React, { createContext, useState, useEffect } from 'react';
import { getAccessToken, login as loginService, logout as logoutService } from '../services/authService';
import { jwtDecode } from "jwt-decode";

export const AuthContext = createContext();

const isTokenExpired = (token) => {
  const decodedToken = jwtDecode(token);
  const currentTime = Date.now() / 1000;
  return decodedToken.exp < currentTime;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = getAccessToken();
    if (token && !isTokenExpired(token)) {
      const decodedToken = jwtDecode(token);
      setUser({ ...decodedToken, token });
    } else {
      handleLogout();
    }
  }, []);

  const isAuthenticated = () => !!getAccessToken();
  const getUserRole = () => localStorage.getItem('role');

  const handleLogin = async (username, password) => {
    const data = await loginService(username, password);
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('role', data.role);
    setUser({ token: data.access });
  };

  const handleLogout = async () => {
    await logoutService();
    localStorage.removeItem('access_token');
    localStorage.removeItem('role');
    setUser(null);
  };

  // Dynamic redirect function based on user role
  const getDashboardPath = (role) => {
    switch (role) {
      case 'CEO':
        return '/dashboard/ceo';
      case 'Employer':
        return '/dashboard/employer';
      case 'Employee':
        return '/dashboard/employee';
      default:
        return '/login';  // Fallback to login if role is not recognized
    }
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, getUserRole, handleLogout, handleLogin, getDashboardPath }}>
      {children}
    </AuthContext.Provider>
  );
};
