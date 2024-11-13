import axios from 'axios';
import { getAccessToken } from './authService';

const API_URL = 'http://localhost:8000/api';

// Default headers for Auth
const authHeaders = () => ({ 
  headers: { Authorization: `Bearer ${getAccessToken()}`} 
});

// List - GET_all
export const getSessions = async () => {
  const response = await axios.get(`${API_URL}/training-sessions/`, authHeaders());
  return response.data;
};

// Retrieve - GET_by_id
export const getSessionDetails = async (sessionId) => {
  const response = await axios.get(`${API_URL}/training-sessions/${sessionId}/`, authHeaders());
  return  response.data;
}

// Create - POST
export const createSession = async (sessionData) => {
  const response = await axios.post(`${API_URL}/training-sessions/`, sessionData, authHeaders());
  return response.data;
}

// Update - PUT_by_id
export const updateSession = async (sessionId, sessionData) => {
  const response = await axios.put(`${API_URL}/training-sessions/${sessionId}/`, sessionData, authHeaders());
  return response.data;
}

// Delete - DELETE_by_id
export const deleteSession = async (sessionId) => {
  const response = await axios.delete(`${API_URL}/training-sessions/${sessionId}`, authHeaders());
  return response.status === 204;
}