import axios from 'axios';
import { UserPublic, Token, Message, ClinicalInsight, Questionnaire, Answer } from '../types/api';

// Use environment variable for backend URL
// During development, Vite will proxy requests from /api to your backend
// In production, this should be the deployed backend URL
const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'; // Default for local dev

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Auth Endpoints ---
export const registerUser = async (username: string, password: string, email?: string): Promise<UserPublic> => {
  const response = await api.post('/register', { username, password, email });
  return response.data as UserPublic;
};

export const loginUser = async (username: string, password: string): Promise<Token> => {
  // FastAPI expects form data for OAuth2PasswordBearer by default,
  // but we are using JSON payload for simplicity in `main.py`
  const response = await api.post('/token', { username, password });
  return response.data as Token;
};

// --- Message Endpoints ---
export const getMessages = async (token: string): Promise<Message[]> => {
  const response = await api.get('/messages/', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data as Message[];
};

export const createMessage = async (token: string, content: string): Promise<Message> => {
  const response = await api.post('/messages/', { content }, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data as Message;
};

// --- Questionnaire Endpoints ---
export const getQuestionnaires = async (token: string): Promise<Questionnaire[]> => {
  const response = await api.get('/questionnaires/active', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data as Questionnaire[];
};

export const submitQuestionnaireAnswer = async (token: string, questionnaireId: number, answers: Answer[]): Promise<any> => {
  const response = await api.post(`/questionnaires/${questionnaireId}/answer`, { answers }, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

// --- Clinical Insight Endpoints ---
export const getInsights = async (token: string): Promise<ClinicalInsight[]> => {
  const response = await api.get('/insights/', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data as ClinicalInsight[];
};

// You might not call this directly from frontend, but it's here for completeness if an admin UI exists
export const createInsight = async (token: string, insightData: ClinicalInsight): Promise<ClinicalInsight> => {
  const response = await api.post('/insights/', insightData, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data as ClinicalInsight;
};