import api from './api';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
}

export const authService = {
  // Test API connection
  testApi: async () => {
    try {
      const response = await api.get('/accounts/api-test/');
      return response.data;
    } catch (error) {
      console.error('API test failed:', error);
      throw error;
    }
  },

  // Register new user
  register: async (data: RegisterData) => {
    try {
      console.log('Registering with data:', data);
      const response = await api.post('/accounts/register/', data);
      console.log('Registration response:', response.data);
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
      }
      return response.data;
    } catch (error: any) {
      console.error('Registration failed:', error);
      console.error('Error details:', error.response?.data);
      throw error;
    }
  },

  // Login
  login: async (credentials: LoginCredentials) => {
    try {
      const response = await api.post('/accounts/login/', credentials);
      if (response.data.access_token) {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
      }
      return response.data;
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  },

  // Logout
  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    try {
      if (refreshToken) {
        await api.post('/accounts/logout/', { refresh_token: refreshToken });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  },

  // Get profile data
  getProfile: async () => {
    try {
      const response = await api.get('/accounts/profile/');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch profile:', error);
      throw error;
    }
  },

  // Get dashboard data
  getDashboard: async () => {
    try {
      const response = await api.get('/accounts/dashboard/');
      return response.data;
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      throw error;
    }
  },

  // Check if user is authenticated
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token');
  },

  // Get token
  getToken: (): string | null => {
    return localStorage.getItem('access_token');
  },
};
