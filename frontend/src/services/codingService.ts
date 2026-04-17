import api from './api';

export interface CodingQuestion {
  id: number;
  title: string;
  description: string;
  difficulty: string;
  difficulty_display: string;
  topic: string;
  topic_display: string;
  sample_input: string;
  sample_output: string;
  explanation: string;
  youtube_link: string | null;
  constraints?: string;
  test_cases?: any[];
  is_solved: boolean;
  is_bookmarked: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserProgressStats {
  total_attempted: number;
  solved: number;
  bookmarked: number;
  by_difficulty: {
    Easy: number;
    Medium: number;
    Hard: number;
  };
}

export const codingService = {
  /**
   * Get all coding questions with optional filters
   */
  async getCodingQuestions(options?: { 
    difficulty?: string; 
    topic?: string; 
   search?: string 
  }): Promise<CodingQuestion[]> {
   const params = new URLSearchParams();
    if (options?.difficulty) params.append('difficulty', options.difficulty);
    if (options?.topic) params.append('topic', options.topic);
    if (options?.search) params.append('search', options.search);
    
   const response = await api.get(`/coding-questions/?${params.toString()}`);
   return response.data;
  },

  /**
   * Get a specific coding question by ID
   */
  async getCodingQuestionById(id: number): Promise<CodingQuestion> {
   const response = await api.get(`/coding-questions/${id}/`);
   return response.data;
  },

  /**
   * Mark a question as solved
   */
  async markAsSolved(id: number): Promise<any> {
   const response = await api.post(`/coding-questions/${id}/mark_solved/`);
   return response.data;
  },

  /**
   * Bookmark a question
   */
  async bookmarkQuestion(id: number): Promise<any> {
   const response = await api.post(`/coding-questions/${id}/bookmark/`);
   return response.data;
  },

  /**
   * Remove bookmark from a question
   */
  async removeBookmark(id: number): Promise<any> {
   const response = await api.post(`/coding-questions/${id}/remove_bookmark/`);
   return response.data;
  },

  /**
   * Get user's progress statistics
   */
  async getUserStats(): Promise<UserProgressStats> {
   const response = await api.get('/user-progress/stats/');
   return response.data;
  },

  /**
   * Get user's bookmarked questions
   */
  async getBookmarkedQuestions(): Promise<any[]> {
   const response = await api.get('/user-progress/bookmarked/');
   return response.data;
  },

  /**
   * Get user's solved questions
   */
  async getSolvedQuestions(): Promise<any[]> {
   const response = await api.get('/user-progress/solved/');
   return response.data;
  },
};
