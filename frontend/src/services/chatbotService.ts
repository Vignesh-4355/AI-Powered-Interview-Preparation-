import api from './api';

export interface ChatMessage {
  id?: number;
  message: string;
  response: string;
  category: string;
  timestamp: string;
  suggestions?: string[];
}

export const chatbotService = {
  async sendMessage(message: string, sessionId?: string): Promise<ChatMessage> {
    const response = await api.post('/chatbot/', {
      message,
      session_id: sessionId
    });
    return response.data;
  },

  async getHistory(limit: number = 50): Promise<ChatMessage[]> {
    const response = await api.get('/chatbot/history/', {
      params: { limit }
    });
    return response.data;
  },
};
