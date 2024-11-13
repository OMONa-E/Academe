import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const login = async (username, password) => {
    try {
        const response = await axios.post(`${API_URL}/token/`, { username, password });
        if (response.data.access) {
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            localStorage.setItem('role', response.data.role);
        }
        return response.data;
    } catch (error) {
        console.error("Login failed:", error);
        throw error;
    }
};

export const logout = async () => {
    const refreshToken = localStorage.getItem('refresh_token');

    if (refreshToken) {
        try {
            await axios.post(`${API_URL}/logout/`, { refresh: refreshToken }, {
                headers: { Authorization: `Bearer ${getAccessToken()}` }
            });
        } catch (error) {
            console.error('Logout failed:', error);
            throw error;
        }
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('role');
};

export const getAccessToken = () => localStorage.getItem('access_token');

export const isAuthenticated = () => !!getAccessToken();

export const getUserRole = () => localStorage.getItem('role');

export const registerEmployee = async (employeeData) => {
    try {
        const response = await axios.post(`${API_URL}/register/employee/`, employeeData);
        return response.data;
    } catch (error) {
        console.error("Error during employee registration:", error);
        throw error;
    }
};

export const registerEmployer = async (employerData) => {
    try {
        const response = await axios.post(`${API_URL}/register/employer/`, employerData);
        return response.data;
    } catch (error) {
        console.error("Error during employer registration:", error);
        throw error;
    }
};