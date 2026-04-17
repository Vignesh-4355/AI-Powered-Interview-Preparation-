import api from './api';

export interface HRQuestion {
  id: number;
  question: string;
  category: string;
  category_display: string;
  sample_answer: string;
  tips: string;
}

export interface GDTopic {
  id: number;
  topic: string;
  type: string;
  type_display: string;
  introduction_points: string;
  arguments_for: string;
  arguments_against: string;
  dos_and_donts: string;
  conclusion_points: string;
}

export const hrgdService = {
  // HR Questions
  async getHRQuestions(category?: string): Promise<HRQuestion[]> {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    
    const response = await api.get(`/hr-questions/?${params.toString()}`);
    return response.data;
  },

  async getHRQuestion(id: number): Promise<HRQuestion> {
    const response = await api.get(`/hr-questions/${id}/`);
    return response.data;
  },

  // GD Topics
  async getGDTopics(type?: string): Promise<GDTopic[]> {
    const params = new URLSearchParams();
    if (type) params.append('type', type);
    
    const response = await api.get(`/gd-topics/?${params.toString()}`);
    return response.data;
  },

  async getGDTopic(id: number): Promise<GDTopic> {
    const response = await api.get(`/gd-topics/${id}/`);
    return response.data;
  },
};
