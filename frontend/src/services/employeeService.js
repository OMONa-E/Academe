import axios from 'axios';
import { getAccessToken } from './authService';

const API_URL = 'http://localhost:8000/api';

// Default headers for Auth
const authHeaders = () => ({ 
  headers: { Authorization: `Bearer ${getAccessToken()}`} 
});

// List - GET_all
export const getEmployee = async () => {
  const response = await axios.get(`${API_URL}/employees/`, authHeaders());
  return response.data;
};

// Retrieve - GET_by_id
export const getEmployeeDetails = async (employeeId) => {
  const response = await axios.get(`${API_URL}/employees/${employeeId}/`, authHeaders());
  return  response.data;
}

// Update - PUT_by_id
export const updateEmployee = async (employeeId, employeeData) => {
  const response = await axios.put(`${API_URL}/employees/${employeeId}/update/`, employeeData, authHeaders());
  return response.data;
}

// Delete - DELETE_by_id
export const deleteEmployee = async (employeeId) => {
  const response = await axios.delete(`${API_URL}/employees/${employeeId}/delete/`, authHeaders());
  return response.status === 204;
}