import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const login = async (username, password) => {
    const response = await axios.post(`${API_URL}/token/`, { username, password });
    if (response.data.access) {
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        localStorage.setItem('role', response.data.role);
    }
    return response.data;
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
            
        }
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
};

export const getAccessToken = () => localStorage.getItem('access_token');

export const isAuthenticated = () => !!getAccessToken();

export const getUserRole = () => localStorage.getItem('role');