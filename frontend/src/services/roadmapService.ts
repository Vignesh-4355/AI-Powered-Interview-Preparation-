import api from './api';

export interface RoadmapItem {
  id: number;
  topic: string;
  description: string;
  status: string;
  status_display: string;
  priority: string;
  priority_display: string;
  category: string;
  category_display: string;
  estimated_hours: number;
  order: number;
}

export const roadmapService = {
  async getRoadmap(): Promise<RoadmapItem[]> {
    const response = await api.get('/roadmap/');
    return response.data;
  },

  async generateRoadmap(): Promise<RoadmapItem[]> {
    const response = await api.get('/roadmap/generate/');
    return response.data;
  },

  async markCompleted(id: number): Promise<any> {
    const response = await api.post(`/roadmap/${id}/mark_completed/`);
    return response.data;
  },

  async markInProgress(id: number): Promise<any> {
    const response = await api.post(`/roadmap/${id}/mark_in_progress/`);
    return response.data;
  },

  async getProgress(): Promise<any> {
    const response = await api.get('/roadmap/progress/');
    return response.data;
  },
};
