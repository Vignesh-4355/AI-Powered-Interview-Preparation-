import api from './api';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface Company {
  id: number;
  name: string;
  description: string;
  logo: string | null;
  industry: string;
  difficulty_level: string;
  difficulty_display: string;
  hiring_frequency: string;
  hiring_frequency_display: string;
  total_questions: number;
  website?: string | null;
}

export interface InterviewPattern {
  id: number;
  round_name: string;
  round_name_display: string;
  description: string;
  duration: string;
  order: number;
}

export interface CompanyDetail extends Company {
  website: string | null;
  interview_patterns: Array<{
    id: number;
    round_name: string;
    round_name_display: string;
    description: string;
    duration: string;
    order: number;
  }>;
  questions_count: number;
}

export interface CompanyQuestion {
  id: number;
  question: string;
  question_type: string;
  question_type_display: string;
  answer: string;
  youtube_link: string | null;
  difficulty: string;
  difficulty_display: string;
  tags: string;
  created_at: string;
}

export const companyService = {
  // Get all companies
  getAllCompanies: async (): Promise<Company[]> => {
    const response = await api.get('/companies/');
    return response.data;
  },

  // Get single company details
  getCompanyDetail: async (id: number): Promise<CompanyDetail> => {
    const response = await api.get(`/companies/${id}/`);
    return response.data;
  },

  // Get company interview patterns
  getCompanyPatterns: async (id: number) => {
    const response = await api.get(`/companies/${id}/patterns/`);
    return response.data;
  },

  // Get company questions
  getCompanyQuestions: async (id: number, params?: { type?: string; difficulty?: string }): Promise<CompanyQuestion[]> => {
    const response = await api.get(`/companies/${id}/questions/`, { params });
    return response.data;
  },

  // Search companies
  searchCompanies: async (query: string): Promise<Company[]> => {
    const response = await api.get('/companies/', {
      params: { search: query }
    });
    return response.data;
  },

  // Get company preparation strategy
  getCompanyStrategy: async (id: number) => {
    const response = await api.get(`/companies/${id}/strategy/`);
    return response.data;
  },

  // Get company learning resources
  getCompanyResources: async (id: number) => {
    const response = await api.get(`/companies/${id}/resources/`);
    return response.data;
  },

  // Get company interview tips
  getCompanyTips: async (id: number) => {
    const response = await api.get(`/companies/${id}/tips/`);
    return response.data;
  },
};
