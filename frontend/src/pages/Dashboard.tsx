import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authService } from '../services/authService';
import { DashboardCard } from '../components/DashboardCard';
import {
  Building2,
  Code2,
  BrainCircuit,
  Users,
  Video,
  Map,
  BarChart3,
  Lightbulb,
  MessageSquare,
  FileCheck
} from 'lucide-react';
import './Dashboard.css';

interface UserProfile {
  target_job_role?: string;
  experience_level?: string;
  bio?: string;
}

interface DashboardData {
  user: {
    email: string;
    first_name?: string;
    last_name?: string;
  };
  profile?: UserProfile | null;
}

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const data = await authService.getDashboard();
        setDashboardData(data);
      } catch (err: any) {
        setError('Failed to load dashboard data');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading your dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>🎯 Interview Prep Dashboard</h1>
          <div className="user-menu">
            <span className="user-email">{user?.email}</span>
            <button onClick={handleLogout} className="btn-logout">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        <div className="welcome-section">
          <h2>
            Welcome back, {dashboardData?.user.first_name || dashboardData?.user.email.split('@')[0]}!
          </h2>
          <p>Ready to ace your next interview?</p>
        </div>

        {dashboardData?.profile && (
          <div className="profile-summary">
            <h3>Your Profile</h3>
            <div className="profile-info">
              {dashboardData.profile.target_job_role && (
                <div className="info-item">
                  <strong>Target Role:</strong> {dashboardData.profile.target_job_role}
                </div>
              )}
              {dashboardData.profile.experience_level && (
                <div className="info-item">
                  <strong>Experience Level:</strong> {dashboardData.profile.experience_level}
                </div>
              )}
            </div>
          </div>
        )}

        <div className="modules-grid">
          <DashboardCard
            title="Company Specific Preparation"
            icon={Building2}
            description="Select a company and get tailored interview questions, patterns, and preparation strategies."
            buttonText="Choose Company"
            to="/companies-list"
            color="#667eea"
          />

          <DashboardCard
            title="Coding Practice"
            icon={Code2}
            description="Practice coding problems from easy to hard. Master data structures and algorithms with hands-on exercises."
            buttonText="Start Coding"
            to="/coding-practice"
            color="#48bb78"
          />

          <DashboardCard
            title="Aptitude Preparation"
            icon={BrainCircuit}
            description="Sharpen your quantitative, logical, and verbal reasoning skills with comprehensive aptitude tests."
            buttonText="Practice Aptitude"
            to="/aptitude"
            color="#ed8936"
          />

          <DashboardCard
            title="HR & Group Discussion"
            icon={Users}
            description="Master behavioral interviews, group discussions, and HR rounds with expert guidance and practice scenarios."
            buttonText="Start Practice"
            to="/hr-discussion"
            color="#e53e3e"
          />

          <DashboardCard
            title="Mock Interviews"
            icon={Video}
            description="Experience real interview simulations with AI feedback. Improve your performance with detailed analytics."
            buttonText="Take Mock Interview"
            to="/mock-interview"
            color="#9f7aea"
          />

          <DashboardCard
            title="AI Chatbot Assistance"
            icon={MessageSquare}
            description="Get instant answers to your questions. 24/7 AI-powered assistance for all your interview prep needs."
            buttonText="Chat Now"
            to="/chatbot"
            color="#4299e1"
          />

          <DashboardCard
            title="Personalized Roadmap"
            icon={Map}
            description="Follow a customized learning path tailored to your target role and experience level."
            buttonText="View Roadmap"
            to="/roadmap"
            color="#38b2ac"
          />

          <DashboardCard
            title="Progress Analytics"
            icon={BarChart3}
            description="Track your preparation progress with detailed insights, charts, and performance metrics."
            buttonText="View Analytics"
            to="/analytics"
            color="#d69e2e"
          />

          <DashboardCard
            title="Expert Tips"
            icon={Lightbulb}
            description="Learn from industry experts with curated tips, tricks, and strategies for interview success."
            buttonText="Explore Tips"
            to="/expert-tips"
            color="#f56565"
          />

          <DashboardCard
            title="Resume Analyzer"
            icon={FileCheck}
            description="Get AI-powered feedback on your resume. Identify missing skills, keywords, and improve your ATS score."
            buttonText="Analyze Resume"
            to="/resume-analyzer"
            color="#ed64a6"
          />
        </div>

        <div className="quick-stats">
          <h3>Quick Stats</h3>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-number">0</div>
              <div className="stat-label">Interviews Completed</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">0</div>
              <div className="stat-label">Questions Practiced</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">0</div>
              <div className="stat-label">Days Active</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">0%</div>
              <div className="stat-label">Success Rate</div>
            </div>
          </div>
        </div>
      </main>

      <footer className="dashboard-footer">
        <p>&copy; 2026 AI Powered Interview Preparation Portal</p>
      </footer>
    </div>
  );
};

export default Dashboard;
