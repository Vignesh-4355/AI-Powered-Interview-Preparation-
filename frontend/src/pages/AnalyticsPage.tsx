import { useState, useEffect } from 'react';
import { 
  BarChart, Bar, PieChart, Pie, Cell, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area 
} from 'recharts';
import { analyticsService } from '../services/analyticsService';
import './AnalyticsPage.css';

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'];

const AnalyticsPage = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const analyticsData = await analyticsService.getAnalytics();
      setData(analyticsData);
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading-container"><div className="spinner">Loading analytics...</div></div>;
  }

  if (!data) {
    return <div className="no-data">No analytics data available</div>;
  }

  // Prepare chart data
  const codingDifficultyData = Object.entries(data.coding_stats?.by_difficulty || {}).map(([key, value]: any) => ({
    name: key,
    attempted: value.count || 0,
    solved: value.solved || 0,
  }));

  const aptitudeCategoryData = Object.entries(data.aptitude_stats?.by_category || {}).map(([key, value]: any) => ({
    name: key,
    accuracy: value.accuracy || 0,
  }));

  const activityTrendData = data.coding_stats?.recent_activity?.map((item: any) => ({
    date: new Date(item.date).toLocaleDateString(),
    count: item.count,
  })) || [];

  const roadmapStatusData = [
    { name: 'Completed', value: data.roadmap_stats?.status_breakdown?.completed || 0 },
    { name: 'In Progress', value: data.roadmap_stats?.status_breakdown?.in_progress || 0 },
    { name: 'Not Started', value: data.roadmap_stats?.status_breakdown?.not_started || 0 },
  ];

  return (
    <div className="analytics-page">
      <div className="page-header">
        <h1>Your Progress Analytics</h1>
        <p className="subtitle">Track your interview preparation journey</p>
      </div>

      {/* Overview Stats Cards */}
      <div className="stats-overview">
        <div className="stat-card primary">
          <div className="stat-icon">📚</div>
          <div className="stat-content">
            <h3>Coding Solved</h3>
            <div className="stat-value">{data.coding_stats?.total_solved || 0}</div>
            <div className="stat-subtitle">out of {data.coding_stats?.total_attempted || 0} attempted</div>
          </div>
        </div>

        <div className="stat-card success">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <h3>Aptitude Accuracy</h3>
            <div className="stat-value">{data.aptitude_stats?.overall_accuracy?.toFixed(1) || 0}%</div>
            <div className="stat-subtitle">{data.aptitude_stats?.total_correct || 0} correct answers</div>
          </div>
        </div>

        <div className="stat-card warning">
          <div className="stat-icon">🎬</div>
          <div className="stat-content">
            <h3>Mock Interviews</h3>
            <div className="stat-value">{data.mock_interview_stats?.completed_sessions || 0}</div>
            <div className="stat-subtitle">Avg score: {data.mock_interview_stats?.average_score?.toFixed(1) || 0}</div>
          </div>
        </div>

        <div className="stat-card info">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>Roadmap Progress</h3>
            <div className="stat-value">{data.roadmap_stats?.completion_percentage?.toFixed(0) || 0}%</div>
            <div className="stat-subtitle">{data.roadmap_stats?.status_breakdown?.completed || 0} tasks completed</div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-grid">
        {/* Coding Difficulty Chart */}
        <div className="chart-card full-width">
          <h2>Coding Progress by Difficulty</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={codingDifficultyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="name" stroke="#666" />
              <YAxis stroke="#666" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}
              />
              <Legend />
              <Bar dataKey="attempted" fill="#667eea" name="Attempted" radius={[4, 4, 0, 0]} />
              <Bar dataKey="solved" fill="#43e97b" name="Solved" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Activity Trend */}
        <div className="chart-card">
          <h2>7-Day Activity Trend</h2>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={activityTrendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="date" stroke="#666" tick={{fontSize: 12}} />
              <YAxis stroke="#666" />
              <Tooltip 
                contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}
              />
              <Area type="monotone" dataKey="count" stroke="#667eea" fill="url(#colorCount)" strokeWidth={2} />
              <defs>
                <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#667eea" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#667eea" stopOpacity={0}/>
                </linearGradient>
              </defs>
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Roadmap Status */}
        <div className="chart-card">
          <h2>Roadmap Status</h2>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={roadmapStatusData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {roadmapStatusData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Aptitude Accuracy by Category */}
        <div className="chart-card full-width">
          <h2>Aptitude Accuracy by Category</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={aptitudeCategoryData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis type="number" domain={[0, 100]} stroke="#666" />
              <YAxis dataKey="name" type="category" stroke="#666" tick={{fontSize: 11}} width={120} />
              <Tooltip 
                formatter={(value) => `${Number(value).toFixed(1)}%`}
                contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}
              />
              <Bar dataKey="accuracy" fill="#764ba2" name="Accuracy %" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Progress Bars Section */}
      <div className="progress-section">
        <h2>Detailed Progress</h2>
        
        <div className="progress-item">
          <div className="progress-header">
            <span>Coding Mastery</span>
            <span>{data.coding_stats?.accuracy?.toFixed(1) || 0}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill coding" 
              style={{ width: `${data.coding_stats?.accuracy || 0}%` }}
            />
          </div>
        </div>

        <div className="progress-item">
          <div className="progress-header">
            <span>Aptitude Skills</span>
            <span>{data.aptitude_stats?.overall_accuracy?.toFixed(1) || 0}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill aptitude" 
              style={{ width: `${data.aptitude_stats?.overall_accuracy || 0}%` }}
            />
          </div>
        </div>

        <div className="progress-item">
          <div className="progress-header">
            <span>Mock Interview Performance</span>
            <span>{((data.mock_interview_stats?.average_score || 0) / 100 * 100).toFixed(1)}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill mock" 
              style={{ width: `${(data.mock_interview_stats?.average_score || 0)}%` }}
            />
          </div>
        </div>

        <div className="progress-item">
          <div className="progress-header">
            <span>Roadmap Completion</span>
            <span>{data.roadmap_stats?.completion_percentage?.toFixed(0) || 0}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill roadmap" 
              style={{ width: `${data.roadmap_stats?.completion_percentage || 0}%` }}
            />
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="recent-activity-section">
        <h2>Recent Activity</h2>
        <div className="activity-list">
          {data.recent_activity?.length > 0 ? (
            data.recent_activity.map((activity: any, idx: number) => (
              <div key={idx} className="activity-item">
                <div className="activity-icon">{activity.icon === 'code' ? '💻' : '🎬'}</div>
                <div className="activity-content">
                  <div className="activity-description">{activity.description}</div>
                  <div className="activity-time">{new Date(activity.timestamp).toLocaleString()}</div>
                </div>
              </div>
            ))
          ) : (
            <div className="no-activity">No recent activity</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;
