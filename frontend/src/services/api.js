import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const normalizedApiBase = API_BASE_URL.replace(/\/+$|^\s+|\s+$/g, '');
const PREDICT_PATH = normalizedApiBase.endsWith('/api') ? '/predict' : '/api/predict';
const finalPredictionUrl = `${normalizedApiBase}${PREDICT_PATH}`;

const api = axios.create({
  baseURL: normalizedApiBase,
  timeout: 30000,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      console.error('Unauthorized');
    }
    return Promise.reject(error);
  }
);

export const predictDisease = async (imageFile) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  
  console.log('Prediction URL:', finalPredictionUrl);
  const response = await axios.post(finalPredictionUrl, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export const getModels = async () => {
  const response = await api.get('/models');
  return response.data;
};

export default api;
