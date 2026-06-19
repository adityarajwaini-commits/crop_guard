import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const normalizeUrl = (url) => url.replace(/^\s+|\s+$/g, '').replace(/\/+$/g, '');
const normalizedApiBase = normalizeUrl(API_BASE_URL);

const buildApiUrls = (baseUrl) => {
  if (baseUrl.endsWith('/api/predict')) {
    return {
      apiRootUrl: baseUrl.slice(0, -'/predict'.length),
      finalPredictionUrl: baseUrl,
    };
  }

  if (baseUrl.endsWith('/api')) {
    return {
      apiRootUrl: baseUrl,
      finalPredictionUrl: `${baseUrl}/predict`,
    };
  }

  return {
    apiRootUrl: `${baseUrl}/api`,
    finalPredictionUrl: `${baseUrl}/api/predict`,
  };
};

const { apiRootUrl, finalPredictionUrl } = buildApiUrls(normalizedApiBase);

const api = axios.create({
  baseURL: apiRootUrl,
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
