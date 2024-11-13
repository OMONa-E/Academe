import axios from 'axios';
import { getAccessToken } from './authService';

const API_URL = 'http://localhost:8000/api';

// Default headers for Auth
const authHeaders = () => ({ 
  headers: { Authorization: `Bearer ${getAccessToken()}`} 
});

// List - GET all employees
export const getEmployee = async () => {
  try {
    const response = await axios.get(`${API_URL}/employees/`, authHeaders());
    return response.data;
  } catch (error) {
    console.error("Error fetching employees:", error);
    throw error;
  }
};

// Retrieve - GET employee by ID
export const getEmployeeDetails = async (employeeId) => {
  try {
    const response = await axios.get(`${API_URL}/employees/${employeeId}/`, authHeaders());
    return response.data;
  } catch (error) {
    console.error(`Error fetching details for employee ID ${employeeId}:`, error);
    throw error;
  }
};

// Update - PUT employee by ID
export const updateEmployee = async (employeeId, employeeData) => {
  try {
    const response = await axios.put(`${API_URL}/employees/${employeeId}/update/`, employeeData, authHeaders());
    return response.data;
  } catch (error) {
    console.error(`Error updating employee with ID ${employeeId}:`, error);
    throw error;
  }
};

// Delete - DELETE employee by ID
export const deleteEmployee = async (employeeId) => {
  try {
    const response = await axios.delete(`${API_URL}/employees/${employeeId}/delete/`, authHeaders());
    return response.status === 204;
  } catch (error) {
    console.error(`Error deleting employee with ID ${employeeId}:`, error);
    throw error;
  }
};

// Get assigned clients for a specific employee
export const getAssignedClients = async (employeeId) => {
  try {
    const response = await axios.get(`${API_URL}/employees/${employeeId}/clients/`, authHeaders());
    return response.data;
  } catch (error) {
    console.error(`Error fetching assigned clients for employee ID ${employeeId}:`, error);
    throw error;
  }
};

// Get upcoming sessions for a specific employee
export const getUpcomingSessions = async (employeeId) => {
  try {
    const response = await axios.get(`${API_URL}/employees/${employeeId}/sessions/`, authHeaders());
    return response.data;
  } catch (error) {
    console.error(`Error fetching upcoming sessions for employee ID ${employeeId}:`, error);
    throw error;
  }
};
