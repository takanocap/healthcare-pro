// services/agentService.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface PatientData {
  id: string;
  name: string;
  condition: string;
  language: string;
  last_checkin?: string;
}

export interface AgentInteractionRequest {
  patient_id: string;
  interaction_type: 'checkin' | 'questionnaire' | 'trend_analysis';
  patient_data: PatientData;
  user_message?: string;
}

export interface PatientInteractionRequest {
  patient_id: string;
  interaction_type: string;
  patient_data: PatientData;
  user_message?: string;
}

export interface AgentResponse {
  agent_response: {
    message: string;
    next_action?: string;
    patient_id: string;
  };
  next_action?: string;
  metadata?: any;
}

export interface PatientInteractionResponse {
  agent_response: {
    message: string;
    next_action?: string;
    patient_id: string;
  };
  next_action?: string;
  metadata?: any;
}

class AgentService {
  private apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  async interactWithAgent(request: PatientInteractionRequest): Promise<PatientInteractionResponse> {
    try {
      console.log("request: ", request);
      const response = await this.apiClient.post('/api/agent/interact', request);
      console.log("response: ", response);
      return response.data;
    } catch (error) {
      console.error('Agent interaction error:', error);
      throw new Error('Failed to communicate with agent');
    }
  }

  async checkAgentHealth(): Promise<boolean> {
    try {
      const response = await this.apiClient.get('/api/agent/health');
      return response.data.status === 'healthy';
    } catch (error) {
      return false;
    }
  }
}

export const agentService = new AgentService();
