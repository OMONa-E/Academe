import axios from 'axios';
import { getAccessToken } from './authService';

const API_URL = 'http://localhost:8000/api';

// Default headers for Auth
const authHeaders = () => ({ 
  headers: { Authorization: `Bearer ${getAccessToken()}`} 
});

// List - GET_all
export const getAudits = async () => {
  const response = await axios.get(`${API_URL}/audit-logs/`, authHeaders());
  return response.data;
};

// Retrieve - GET_by_id
export const getAuditDetails = async (auditId) => {
  const response = await axios.get(`${API_URL}/audit-logs/${auditId}/`, authHeaders());
  return  response.data;
}

// List - GET_all
export const getActiveSessionAudits = async () => {
    const response = await axios.get(`${API_URL}/active-sessions/`, authHeaders());
    return response.data;
  };
  
  // Retrieve - GET_by_id
  export const getActiveSessionAuditDetails = async (auditId) => {
    const response = await axios.get(`${API_URL}/active-sessions/${auditId}/`, authHeaders());
    return  response.data;
  }
