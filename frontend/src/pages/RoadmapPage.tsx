import { useState, useEffect } from 'react';
import { Map, CheckCircle, PlayCircle, RefreshCw, Trophy, Target } from 'lucide-react';
import { roadmapService, type RoadmapItem as RoadmapItemType } from '../services/roadmapService';
import './RoadmapPage.css';

const RoadmapPage = () => {
  const [roadmapItems, setRoadmapItems] = useState<RoadmapItemType[]>([]);
  const [progress, setProgress] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadRoadmap();
  }, []);

  const loadRoadmap = async () => {
    try {
      const items = await roadmapService.getRoadmap();
      setRoadmapItems(items);
      const progressData = await roadmapService.getProgress();
      setProgress(progressData);
    } catch (error) {
      console.error('Error loading roadmap:', error);
    }
  };

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const items = await roadmapService.generateRoadmap();
      setRoadmapItems(items);
      const progressData = await roadmapService.getProgress();
      setProgress(progressData);
      alert('Personalized roadmap generated successfully!');
    } catch (error) {
      alert('Failed to generate roadmap');
    }
    setLoading(false);
  };

  const handleMarkCompleted = async (id: number) => {
    try {
      await roadmapService.markCompleted(id);
      loadRoadmap();
    } catch (error) {
      alert('Failed to mark as completed');
    }
  };

  const handleMarkInProgress = async (id: number) => {
    try {
      await roadmapService.markInProgress(id);
      loadRoadmap();
    } catch (error) {
      alert('Failed to mark as in progress');
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Critical': return '#f44336';
      case 'High': return '#ff9800';
      case 'Medium': return '#2196f3';
      case 'Low': return '#4caf50';
      default: return '#9e9e9e';
    }
  };

  const getStatusIcon = (status: string) => {
    if (status === 'Completed') return <CheckCircle size={20} className="completed" />;
    if (status === 'In Progress') return <PlayCircle size={20} className="in-progress" />;
    return <Target size={20} className="not-started" />;
  };

  return (
    <div className="roadmap-page">
      <div className="roadmap-header">
        <div className="header-content">
          <Map size={40} className="icon" />
          <h1>Your Personalized Learning Roadmap</h1>
          <p>AI-generated study plan based on your performance and goals</p>
        </div>
        <button 
          onClick={handleGenerate} 
          disabled={loading}
          className="generate-btn"
        >
          <RefreshCw size={18} className={loading ? 'spinning' : ''} />
          {loading ? 'Generating...' : 'Regenerate Roadmap'}
        </button>
      </div>

      {progress && (
        <div className="progress-overview">
          <div className="progress-card main">
            <Trophy size={32} />
            <div className="progress-info">
              <div className="progress-value">{progress.completion_percentage}%</div>
              <div className="progress-label">Overall Progress</div>
            </div>
          </div>
          <div className="progress-card">
            <div className="stat-value">{progress.completed}</div>
            <div className="stat-label">Completed</div>
          </div>
          <div className="progress-card">
            <div className="stat-value">{progress.in_progress}</div>
            <div className="stat-label">In Progress</div>
          </div>
          <div className="progress-card">
            <div className="stat-value">{progress.not_started}</div>
            <div className="stat-label">To Start</div>
          </div>
        </div>
      )}

      <div className="roadmap-container">
        {roadmapItems.length === 0 ? (
          <div className="empty-state">
            <Map size={64} className="empty-icon" />
            <h2>No Roadmap Yet</h2>
            <p>Click "Regenerate Roadmap" to create your personalized study plan</p>
          </div>
        ) : (
          <div className="roadmap-items">
            {roadmapItems.map((item, idx) => (
              <div 
                key={item.id} 
                className={`roadmap-item ${item.status.toLowerCase().replace(' ', '-')}`}
              >
                <div className="item-number">#{idx + 1}</div>
                <div className="item-content">
                  <div className="item-header">
                    <div className="topic-section">
                      {getStatusIcon(item.status_display)}
                      <h3>{item.topic}</h3>
                    </div>
                    <div 
                      className="priority-badge"
                      style={{ background: getPriorityColor(item.priority) }}
                    >
                      {item.priority}
                    </div>
                  </div>
                  
                  <p className="description">{item.description}</p>
                  
                  <div className="item-meta">
                    <span className="category-tag">{item.category_display}</span>
                    <span className="time-estimate">⏱ {item.estimated_hours} hours</span>
                  </div>
                  
                  {item.status !== 'Completed' && (
                    <div className="item-actions">
                      {item.status === 'Not Started' && (
                        <button 
                          onClick={() => handleMarkInProgress(item.id)}
                          className="action-btn start"
                        >
                          <PlayCircle size={16} />
                          Start Task
                        </button>
                      )}
                      {item.status === 'In Progress' && (
                        <button 
                          onClick={() => handleMarkCompleted(item.id)}
                          className="action-btn complete"
                        >
                          <CheckCircle size={16} />
                          Mark Complete
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default RoadmapPage;
