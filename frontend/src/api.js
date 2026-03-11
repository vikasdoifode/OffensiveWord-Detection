import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api`
  : 'https://offensiveword-detection.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeComment = async (comment) => {
  const response = await api.post('/analyze-comment', { comment });
  return response.data;
};

export const analyzeYouTubeChat = async (url) => {
  const response = await api.post('/analyze-youtube-chat', { url });
  return response.data;
};

export const addWord = async (word) => {
  const response = await api.post('/add-word', { word });
  return response.data;
};

export const getWords = async () => {
  const response = await api.get('/words');
  return response.data;
};

export const getAlgorithms = async () => {
  const response = await api.get('/algorithms');
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
