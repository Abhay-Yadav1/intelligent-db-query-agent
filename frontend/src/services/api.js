import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const queryDatabase = async (question) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/query`, {
      question: question
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export const getTables = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/tables`);
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};