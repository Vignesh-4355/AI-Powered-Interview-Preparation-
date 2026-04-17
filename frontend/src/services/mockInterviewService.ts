import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';

export interface InterviewQuestion {
  id: number;
  question_text: string;
  question_type: string;
  question_type_display: string;
  difficulty: string;
  difficulty_display: string;
  expected_keywords: string[];
  model_answer: string;
  created_at: string;
}

export interface MockInterviewSession {
  id: number;
  user: number;
  interview_type: string;
  interview_type_display: string;
  difficulty: string;
  difficulty_display: string;
  total_questions: number;
  start_time: string;
  end_time: string | null;
  is_completed: boolean;
  score: number | null;
  feedback: string;
  answers_count?: number;
  answers?: UserAnswer[];
}

export interface UserAnswer {
  id: number;
  session: number;
  question: number;
  question_text: string;
  question_type: string;
  answer_text: string;
  timestamp: string;
  keyword_score: number;
  feedback: string;
}

export interface StartInterviewPayload {
  interview_type: 'HR' | 'Technical' | 'Coding' | 'Mixed';
  difficulty: 'Easy' | 'Medium' | 'Hard';
  total_questions?: number;
}

export interface SubmitAnswerPayload {
  session_id: number;
  question_id: number;
  answer_text: string;
}

export interface StartInterviewResponse {
  session: MockInterviewSession;
  question: InterviewQuestion;
  question_number: number;
  total_questions: number;
}

export interface SubmitAnswerResponse {
  completed: boolean;
  question?: InterviewQuestion;
  question_number?: number;
  total_questions?: number;
  previous_feedback?: string;
  session?: MockInterviewSession;
}

export const mockInterviewService = {
  // Start a new interview session
  startInterview: async (payload: StartInterviewPayload): Promise<StartInterviewResponse> => {
    const response = await axios.post(`${API_URL}mock/start/`, payload);
    return response.data;
  },

  // Submit answer and get next question
  submitAnswer: async (payload: SubmitAnswerPayload): Promise<SubmitAnswerResponse> => {
    const response = await axios.post(`${API_URL}mock/answer/`, payload);
    return response.data;
  },

  // Get session results
  getSessionResult: async (sessionId: number): Promise<MockInterviewSession> => {
    const response = await axios.get(`${API_URL}mock/result/${sessionId}/`);
    return response.data;
  },

  // Get user's interview history
  getHistory: async (): Promise<MockInterviewSession[]> => {
    const response = await axios.get(`${API_URL}mock/history/`);
    return response.data;
  },

  // Browse questions
  getQuestions: async (params?: { type?: string; difficulty?: string }): Promise<InterviewQuestion[]> => {
    const response = await axios.get(`${API_URL}mock/questions/`, { params });
    return response.data;
  },
};
