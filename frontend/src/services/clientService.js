import axios from 'axios';
import { getAccessToken } from './authService';

const API_URL = 'http://localhost:8000/api';

// Default headers for Auth
const authHeaders = () => ({ 
  headers: { Authorization: `Bearer ${getAccessToken()}`} 
});

// List - GET_all
export const getClients = async () => {
  const response = await axios.get(`${API_URL}/clients/`, authHeaders());
  return response.data;
};

// Retrieve - GET_by_id
export const getClientDetails = async (clientId) => {
  const response = await axios.get(`${API_URL}/clients/${clientId}/`, authHeaders());
  return  response.data;
}

// Create - POST
export const createClient = async (clientData) => {
  const response = await axios.post(`${API_URL}/clients/`, clientData, authHeaders());
  return response.data;
}

// Update - PUT_by_id
export const updateClient = async (clientId, clientData) => {
  const response = await axios.put(`${API_URL}/clients/${clientId}/`, clientData, authHeaders());
  return response.data;
}

// Delete - DELETE_by_id
export const deleteClient = async (clientId) => {
  const response = await axios.delete(`${API_URL}/clients/${clientId}`, authHeaders());
  return response.status === 204;
}