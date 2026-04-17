import { Link, useNavigate } from 'react-router-dom';
import { BrainCircuit, ArrowLeft, BookOpen, TrendingUp, CheckCircle } from 'lucide-react';
import { aptitudeService, type AptitudeStats } from '../services/aptitudeService';
import { useState, useEffect } from 'react';
import './ModulePage.css';

const Aptitude = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<AptitudeStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [questionCount, setQuestionCount] = useState(0);

  useEffect(() => {
    fetchStats();
    fetchQuestionCount();
  }, []);

  const fetchStats = async () => {
    try {
      const data = await aptitudeService.getStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const fetchQuestionCount = async () => {
    try {
      const questions = await aptitudeService.getAllQuestions();
      setQuestionCount(questions.length);
    } catch (error) {
      console.error('Failed to fetch questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStartPractice = () => {
    navigate('/aptitude/list');
  };

  if (loading) {
    return (
      <div className="module-page-container">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading aptitude questions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="module-page-container">
      <div className="module-header">
        <Link to="/dashboard" className="back-button">
          <ArrowLeft size={20} />
          Back to Dashboard
        </Link>
        <div className="module-icon-large">
          <BrainCircuit size={64} />
        </div>
        <h1>Aptitude Preparation</h1>
        <p className="module-subtitle">
          Sharpen your quantitative, logical, and verbal reasoning skills with comprehensive aptitude tests.
        </p>
      </div>
      
      <div className="module-content">
        {/* Stats Overview */}
        {stats && stats.total_attempts > 0 && (
          <div className="stats-overview" style={{ marginBottom: '2rem' }}>
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

        {/* Practice Section */}
        <div className="coming-soon" style={{ textAlign: 'center' }}>
          <h2 style={{ marginBottom: '1rem' }}>📚 Practice Aptitude Questions</h2>
          <p style={{ fontSize: '1.1rem', color: '#4a5568', marginBottom: '2rem' }}>
            {questionCount > 0 
              ? `We have ${questionCount} aptitude questions across multiple categories including Time & Work, Time & Distance, Percentages, Profit & Loss, Probability, and Logical Reasoning.`
              : 'Aptitude questions will be available soon.'}
          </p>

          {questionCount > 0 && (
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
              gap: '1rem',
              marginBottom: '2rem',
              maxWidth: '800px',
              margin: '0 auto 2rem'
            }}>
              <div style={{ 
                padding: '1rem', 
                background: '#f7fafc', 
                borderRadius: '10px',
                borderLeft: '4px solid #6366f1'
              }}>
                <strong>Time & Work</strong>
                <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.875rem', color: '#718096' }}>
                  Work rates, combined work, efficiency
                </p>
              </div>
              <div style={{ 
                padding: '1rem', 
                background: '#f7fafc', 
                borderRadius: '10px',
                borderLeft: '4px solid #10b981'
              }}>
                <strong>Time & Distance</strong>
                <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.875rem', color: '#718096' }}>
                  Speed, trains, boats & streams
                </p>
              </div>
              <div style={{ 
                padding: '1rem', 
                background: '#f7fafc', 
                borderRadius: '10px',
                borderLeft: '4px solid #f59e0b'
              }}>
                <strong>Percentages</strong>
                <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.875rem', color: '#718096' }}>
                  Percentage change, successive changes
                </p>
              </div>
              <div style={{ 
                padding: '1rem', 
                background: '#f7fafc', 
                borderRadius: '10px',
                borderLeft: '4px solid #ef4444'
              }}>
                <strong>Profit & Loss</strong>
                <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.875rem', color: '#718096' }}>
                  CP, SP, profit/loss percentage
                </p>
              </div>
              <div style={{ 
                padding: '1rem', 
                background: '#f7fafc', 
                borderRadius: '10px',
                borderLeft: '4px solid #8b5cf6'
              }}>
                <strong>Probability</strong>
                <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.875rem', color: '#718096' }}>
                  Combinations, permutations, dice, cards
                </p>
              </div>
              <div style={{ 
                padding: '1rem', 
                background: '#f7fafc', 
                borderRadius: '10px',
                borderLeft: '4px solid #ec4899'
              }}>
                <strong>Logical Reasoning</strong>
                <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.875rem', color: '#718096' }}>
                  Series, patterns, coding-decoding
                </p>
              </div>
            </div>
          )}

          <button
            onClick={handleStartPractice}
            style={{
              padding: '1rem 2rem',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '10px',
              fontSize: '1rem',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            Start Practice
            <ArrowLeft size={20} style={{ transform: 'rotate(180deg)' }} />
          </button>
        </div>
      </div>
    </div>
  );
};

// Fix: Add missing Link import
import { Link } from 'react-router-dom';

export default Aptitude;
