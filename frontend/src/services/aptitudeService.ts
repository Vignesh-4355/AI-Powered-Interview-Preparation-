import api from './api';

export interface AptitudeQuestion {
  id: number;
  question: string;
  category: string;
  category_display: string;
  difficulty: string;
  difficulty_display: string;
  options: string[];
  correct_answer: string;
  solution: string;
  explanation: string;
  formula_used: string;
  youtube_link: string;
  created_at: string;
  updated_at: string;
}

export interface AptitudeQuestionList {
  id: number;
  question: string;
  category: string;
  category_display: string;
  difficulty: string;
  difficulty_display: string;
  options: string[];
}

export interface UserAttempt {
  id: number;
  question: number;
  question_text: string;
  question_category: string;
  selected_answer: string;
  is_correct: boolean;
  time_taken: number | null;
  attempted_at: string;
}

export interface AptitudeStats {
  total_attempts: number;
  correct: number;
  accuracy: number;
  by_category: {
    [key: string]: {
      attempted: number;
      correct: number;
      accuracy: number;
    };
  };
}

export const aptitudeService = {
  // Get all questions with optional filters
  getAllQuestions: async (params?: { category?: string; difficulty?: string }): Promise<AptitudeQuestionList[]> => {
    const response = await api.get('/aptitude/', { params });
    return response.data;
  },

  // Get single question details
  getQuestionDetail: async (id: number): Promise<AptitudeQuestion> => {
    const response = await api.get(`/aptitude/${id}/`);
    return response.data;
  },

  // Get questions by category
  getQuestionsByCategory: async (category: string): Promise<AptitudeQuestionList[]> => {
    const response = await api.get('/aptitude/by_category/', {
      params: { category }
    });
    return response.data;
  },

  // Submit answer
  submitAnswer: async (questionId: number, selectedAnswer: string, timeTaken?: number) => {
    const response = await api.post(`/aptitude/${questionId}/submit_answer/`, {
      selected_answer: selectedAnswer,
      time_taken: timeTaken,
    });
    return response.data;
  },

  // Get user's attempt history
  getUserAttempts: async (): Promise<UserAttempt[]> => {
    const response = await api.get('/user-attempts/');
    return response.data;
  },

  // Get user statistics
  getStats: async (): Promise<AptitudeStats> => {
    const response = await api.get('/user-attempts/stats/');
    return response.data;
  },
};
