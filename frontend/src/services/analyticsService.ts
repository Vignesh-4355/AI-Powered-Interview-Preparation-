import api from './api';

export interface AnalyticsData {
  progress: any;
  coding_stats: any;
  aptitude_stats: any;
  mock_interview_stats: any;
  company_prep_stats: any;
  roadmap_stats: any;
  recent_activity: any[];
}

export const analyticsService = {
  async getAnalytics(): Promise<AnalyticsData> {
    const response = await api.get('/analytics/');
    return response.data;
  },

  async updateProgress(activityType: string, data?: any): Promise<any> {
    const response = await api.post('/analytics/update/', {
      type: activityType,
      ...data
    });
    return response.data;
  },
};
