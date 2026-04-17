import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Brain, TrendingUp, Clock, Percent, PieChart, Puzzle, 
  ArrowRight, BookOpen, CheckCircle, XCircle 
} from 'lucide-react';
import { aptitudeService, type AptitudeStats } from '../services/aptitudeService';
import './AptitudeList.css';

const CATEGORIES = [
  { 
    id: 'Time and Work', 
    name: 'Time & Work', 
    icon: Clock, 
    color: '#6366f1',
    description: 'Work rates, combined work, efficiency problems' 
  },
  { 
    id: 'Time and Distance', 
    name: 'Time & Distance', 
    icon: TrendingUp, 
    color: '#10b981',
    description: 'Speed, relative motion, trains, boats & streams' 
  },
  { 
    id: 'Percentages', 
    name: 'Percentages', 
    icon: Percent, 
    color: '#f59e0b',
    description: 'Percentage change, successive changes, comparisons' 
  },
  { 
    id: 'Profit and Loss', 
    name: 'Profit & Loss', 
    icon: PieChart, 
    color: '#ef4444',
    description: 'Cost price, selling price, profit/loss percentage' 
  },
  { 
    id: 'Probability', 
    name: 'Probability', 
    icon: Brain, 
    color: '#8b5cf6',
    description: 'Events, combinations, permutations, dice, cards' 
  },
  { 
    id: 'Logical Reasoning', 
    name: 'Logical Reasoning', 
    icon: Puzzle, 
    color: '#ec4899',
    description: 'Series, patterns, coding-decoding, analogies' 
  },
];

const AptitudeList = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<AptitudeStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [questionCounts, setQuestionCounts] = useState<{[key: string]: number}>({});

  useEffect(() => {
    fetchStats();
    fetchQuestionCounts();
  }, []);

  const fetchStats = async () => {
    try {
      const data = await aptitudeService.getStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchQuestionCounts = async () => {
    try {
      const questions = await aptitudeService.getAllQuestions();
      const counts: {[key: string]: number} = {};
      questions.forEach(q => {
        counts[q.category] = (counts[q.category] || 0) + 1;
      });
      setQuestionCounts(counts);
    } catch (err) {
      console.error('Failed to fetch questions:', err);
    }
  };

  const handleStartPractice = (categoryId: string) => {
    navigate(`/aptitude/${encodeURIComponent(categoryId)}`);
  };

  const handleRetryWrong = () => {
    navigate('/aptitude/practice?mode=retry');
  };

  const getDifficultyBadge = (categoryId: string) => {
    const counts = questionCounts[categoryId] || 0;
    if (counts === 0) return 'No Questions';
    if (counts < 5) return 'Basic';
    if (counts < 10) return 'Intermediate';
    return 'Advanced';
  };

  return (
    <div className="aptitude-list-page">
      {/* Header */}
      <div className="aptitude-header">
        <h1>
          <Brain size={40} />
          Aptitude Preparation
        </h1>
        <p>Master quantitative aptitude, logical reasoning, and problem-solving skills</p>
      </div>

      {/* Stats Overview */}
      {stats && stats.total_attempts > 0 && (
        <div className="stats-overview">
          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#6366f1' }}>
              <BookOpen size={24} />
            </div>
            <div className="stat-content">
              <h3>{stats.total_attempts}</h3>
              <p>Questions Attempted</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#10b981' }}>
              <CheckCircle size={24} />
            </div>
            <div className="stat-content">
              <h3>{stats.correct}</h3>
              <p>Correct Answers</p>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#f59e0b' }}>
              <TrendingUp size={24} />
            </div>
            <div className="stat-content">
              <h3>{stats.accuracy}%</h3>
              <p>Overall Accuracy</p>
            </div>
          </div>
        </div>
      )}

      {/* Retry Wrong Questions */}
      {stats && stats.total_attempts > 0 && stats.accuracy < 100 && (
        <div className="retry-section">
          <button className="retry-btn" onClick={handleRetryWrong}>
            <XCircle size={20} />
            Retry Wrong Questions ({stats.total_attempts - stats.correct})
          </button>
        </div>
      )}

      {/* Category Grid */}
      <div className="category-grid">
        {CATEGORIES.map((category) => {
          const Icon = category.icon;
          const questionCount = questionCounts[category.id] || 0;
          const categoryStats = stats?.by_category[category.id];
          const accuracy = categoryStats?.accuracy || 0;

          return (
            <div key={category.id} className="category-card">
              <div className="category-header" style={{ background: `linear-gradient(135deg, ${category.color} 0%, ${category.color}dd 100%)` }}>
                <Icon size={48} />
                <h2>{category.name}</h2>
              </div>
              
              <div className="category-body">
                <p className="category-description">{category.description}</p>
                
                <div className="category-stats">
                  <div className="stat-item">
                    <span className="stat-label">Questions</span>
                    <span className="stat-value">{questionCount}</span>
                  </div>
                  <div className="stat-item">
                    <span className="stat-label">Level</span>
                    <span className="stat-value">{getDifficultyBadge(category.id)}</span>
                  </div>
                  {categoryStats && categoryStats.attempted > 0 && (
                    <div className="stat-item">
                      <span className="stat-label">Your Accuracy</span>
                      <span className="stat-value" style={{ color: accuracy >= 70 ? '#10b981' : '#f59e0b' }}>
                        {accuracy}%
                      </span>
                    </div>
                  )}
                </div>

                {categoryStats && categoryStats.attempted > 0 && (
                  <div className="progress-bar-container">
                    <div className="progress-label">
                      <span>Progress</span>
                      <span>{categoryStats.attempted} attempted</span>
                    </div>
                    <div className="progress-bar">
                      <div 
                        className="progress-fill" 
                        style={{ width: `${Math.min(accuracy, 100)}%`, background: category.color }}
                      />
                    </div>
                  </div>
                )}

                <button 
                  className="start-practice-btn"
                  onClick={() => handleStartPractice(category.id)}
                  style={{ 
                    background: questionCount > 0 ? category.color : '#cbd5e1',
                    cursor: questionCount > 0 ? 'pointer' : 'not-allowed'
                  }}
                  disabled={questionCount === 0}
                >
                  {questionCount > 0 ? 'Start Practice' : 'Coming Soon'}
                  <ArrowRight size={18} />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Loading State */}
      {loading && (
        <div className="loading-state">
          <div className="spinner" />
          <p>Loading categories...</p>
        </div>
      )}
    </div>
  );
};

export default AptitudeList;
