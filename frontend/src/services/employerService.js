import axios from 'axios';
import { getAccessToken } from './authService';

const API_URL = 'http://localhost:8000/api';

// Default headers for Auth
const authHeaders = () => ({ 
  headers: { Authorization: `Bearer ${getAccessToken()}`} 
});

// List - GET_all
export const getEmployer = async () => {
  const response = await axios.get(`${API_URL}/employers/`, authHeaders());
  return response.data;
};

// Retrieve - GET_by_id
export const getEmployerDetails = async (employerId) => {
  const response = await axios.get(`${API_URL}/employers/${employerId}/`, authHeaders());
  return  response.data;
}

// Update - PUT_by_id
export const updateEmployer = async (employerId, employerData) => {
  const response = await axios.put(`${API_URL}/employers/${employerId}/update/`, employerData, authHeaders());
  return response.data;
}

// Delete - DELETE_by_id
export const deleteEmployer = async (employerId) => {
  const response = await axios.delete(`${API_URL}/employers/${employerId}/delete/`, authHeaders());
  return response.status === 204;
}

export const getEmployees = async (employerId) => {
  try {
    const response = await axios.get(`${API_URL}/employers/${employerId}/employees/`, {
      headers: { Authorization: `Bearer ${getAccessToken()}` }
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching employees:", error);
    throw error;
  }
};

export const getFinancialData = async (employerId) => {
  try {
    const response = await axios.get(`${API_URL}/employers/${employerId}/financial-data/`, {
      headers: { Authorization: `Bearer ${getAccessToken()}` }
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching financial data:", error);
    throw error;
  }
};