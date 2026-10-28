import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
});

// Request interceptor to add the auth token
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    // Don't set Content-Type for FormData - let axios handle it
    if (config.data instanceof FormData) {
        delete config.headers['Content-Type'];
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export const petService = {
    getAll: (params) => api.get('/animals', { params }),
    getById: (id) => api.get(`/animals/${id}`),
    delete: (id) => api.delete(`/animals/${id}`),
};

export const adoptionService = {
    create: (data) => api.post('/adoptions', data),
    getMyAdoptions: () => api.get('/adoptions/me'),
    getAll: () => api.get('/adoptions'),
};

export const reportService = {
    create: (data) => api.post('/reports', data),
    getAll: () => api.get('/reports'),
};

export default api;
