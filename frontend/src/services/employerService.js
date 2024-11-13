import axios from 'axios';
import { getAccessToken } from './authService';

const API_URL = 'http://localhost:8000/api';

// Default headers for Auth
const authHeaders = () => ({ 
  headers: { Authorization: `Bearer ${getAccessToken()}` } 
});

// List - GET all employers
export const getEmployer = async () => {
  try {
    const response = await axios.get(`${API_URL}/employers/`, authHeaders());
    return response.data;
  } catch (error) {
    console.error("Error fetching employers:", error);
    throw error;
  }
};

// Retrieve - GET employer by ID
export const getEmployerDetails = async (employerId) => {
  try {
    const response = await axios.get(`${API_URL}/employers/${employerId}/`, authHeaders());
    return response.data;
  } catch (error) {
    console.error(`Error fetching employer details for ID ${employerId}:`, error);
    throw error;
  }
};

// Update - PUT employer by ID
export const updateEmployer = async (employerId, employerData) => {
  try {
    const response = await axios.put(`${API_URL}/employers/${employerId}/update/`, employerData, authHeaders());
    return response.data;
  } catch (error) {
    console.error(`Error updating employer with ID ${employerId}:`, error);
    throw error;
  }
};

// Delete - DELETE employer by ID
export const deleteEmployer = async (employerId) => {
  try {
    const response = await axios.delete(`${API_URL}/employers/${employerId}/delete/`, authHeaders());
    return response.status === 204;
  } catch (error) {
    console.error(`Error deleting employer with ID ${employerId}:`, error);
    throw error;
  }
};

// Get employees under a specific employer
export const getEmployees = async (employerId) => {
  try {
    const response = await axios.get(`${API_URL}/employers/${employerId}/employees/`, authHeaders());
    return response.data;
  } catch (error) {
    console.error(`Error fetching employees for employer ID ${employerId}:`, error);
    throw error;
  }
};

// Get financial data for a specific employer
export const getFinancialData = async (employerId) => {
  try {
    const response = await axios.get(`${API_URL}/employers/${employerId}/financial-data/`, authHeaders());
    return response.data;
  } catch (error) {
    console.error(`Error fetching financial data for employer ID ${employerId}:`, error);
    throw error;
  }
};
