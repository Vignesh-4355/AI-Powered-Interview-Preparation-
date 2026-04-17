import api from './api';

export interface ResumeAnalysis {
  id: number;
  resume: number;
  detected_skills: Array<{skill: string; category: string}>;
  missing_skills: Array<{skill: string; category: string; priority: string}>;
  keywords_found: Array<{keyword: string; count: number; density: number}>;
  skill_score: number;
  keyword_density: number;
  formatting_score: number;
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
  ats_score: number;
  ats_issues: string[];
  analyzed_at: string;
}

export interface Resume {
  id: number;
  user: number;
  file: string;
  original_filename: string;
  uploaded_at: string;
  file_size: number;
  file_size_mb: number;
  extracted_text: string;
  analysis?: ResumeAnalysis;
}

export const resumeService = {
  /**
   * Upload and analyze a resume
   */
  async analyzeResume(file: File): Promise<{resume: Resume; analysis: ResumeAnalysis}> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/resume/analyze/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  /**
   * Get user's resume history
   */
  async getResumeHistory(): Promise<Resume[]> {
    const response = await api.get('/resume/history/');
    return response.data;
  },

  /**
   * Get detailed analysis of a specific resume
   */
  async getResumeDetail(resumeId: number): Promise<{resume: Resume; analysis: ResumeAnalysis}> {
    const response = await api.get(`/resume/${resumeId}/`);
    return response.data;
  },
};
