import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, Building2, BookOpen, FileText, Youtube, ExternalLink,
  CheckCircle, HelpCircle, Target, Lightbulb, AlertTriangle, Play,
  Clock, TrendingUp, Award, Star, ChevronDown, ChevronUp, Bookmark, Code
} from 'lucide-react';
import { companyService, type Company, type InterviewPattern, type CompanyQuestion } from '../services/companyService';
import './CompanyDetail.css';

const CompanyDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [company, setCompany] = useState<Company | null>(null);
  const [patterns, setPatterns] = useState<InterviewPattern[]>([]);
  const [questions, setQuestions] = useState<CompanyQuestion[]>([]);
  const [strategy, setStrategy] = useState<any>(null);
  const [resources, setResources] = useState<any>(null);
  const [tips, setTips] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState<'overview' | 'process' | 'questions' | 'strategy' | 'resources' | 'tips'>('overview');
  const [selectedQuestionType, setSelectedQuestionType] = useState<string>('all');
  const [expandedQuestions, setExpandedQuestions] = useState<Set<number>>(new Set());
  const [completedQuestions, setCompletedQuestions] = useState<Set<number>>(new Set());
  const [completedWeeks, setCompletedWeeks] = useState<Set<number>>(new Set());

  useEffect(() => {
    fetchCompanyData();
  }, [id]);

  const fetchCompanyData = async () => {
    try {
      setLoading(true);
      if (!id) return;
      
      const companyId = parseInt(id);
      const [companyData, patternsData, questionsData, strategyData, resourcesData, tipsData] = await Promise.all([
        companyService.getCompanyDetail(companyId),
        companyService.getCompanyPatterns(companyId),
        companyService.getCompanyQuestions(companyId),
        companyService.getCompanyStrategy(companyId),
        companyService.getCompanyResources(companyId),
        companyService.getCompanyTips(companyId)
      ]);
      
      setCompany(companyData);
      setPatterns(patternsData);
      setQuestions(questionsData);
      setStrategy(strategyData);
      setResources(resourcesData);
      setTips(tipsData);
    } catch (err: any) {
      setError('Failed to load company data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleQuestion = (questionId: number) => {
    const newExpanded = new Set(expandedQuestions);
    if (newExpanded.has(questionId)) {
      newExpanded.delete(questionId);
    } else {
      newExpanded.add(questionId);
    }
    setExpandedQuestions(newExpanded);
  };

  const toggleQuestionComplete = (questionId: number) => {
    const newCompleted = new Set(completedQuestions);
    if (newCompleted.has(questionId)) {
      newCompleted.delete(questionId);
    } else {
      newCompleted.add(questionId);
    }
    setCompletedQuestions(newCompleted);
  };

  const toggleWeekComplete = (weekNum: number) => {
    const newCompleted = new Set(completedWeeks);
    if (newCompleted.has(weekNum)) {
      newCompleted.delete(weekNum);
    } else {
      newCompleted.add(weekNum);
    }
    setCompletedWeeks(newCompleted);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return '#10b981';
      case 'medium': return '#f59e0b';
      case 'hard': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'HR': return '👤';
      case 'Technical': return '💻';
      case 'Coding': return '⌨️';
      case 'Aptitude': return '🧮';
      case 'Behavioral': return '🎯';
      default: return '📋';
    }
  };

  if (loading) {
    return (
      <div className="company-detail-container">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading company details...</p>
        </div>
      </div>
    );
  }

  if (error || !company) {
    return (
      <div className="company-detail-container">
        <div className="error-state">
          <h2>Error</h2>
          <p>{error || 'Company not found'}</p>
          <button onClick={() => navigate('/companies-list')} className="back-button">
            <ArrowLeft size={20} />
            Back to Companies
          </button>
        </div>
      </div>
    );
  }

  const progressPercentage = questions.length > 0 
    ? Math.round((completedQuestions.size / questions.length) * 100) 
    : 0;

  return (
    <div className="company-detail-container">
      {/* Header */}
      <div className="detail-header">
        <button onClick={() => navigate('/companies-list')} className="back-button">
          <ArrowLeft size={20} />
          Back to Companies
        </button>
        
        <div className="company-hero">
          <div className="company-hero-content">
            {company.logo ? (
              <img src={company.logo} alt={company.name} className="company-hero-logo" />
            ) : (
              <div className="company-hero-logo-placeholder">
                <Building2 size={64} />
              </div>
            )}
            <div className="company-info">
              <h1>{company.name}</h1>
              <p className="company-industry">{company.industry}</p>
              <div className="company-meta">
                <span className="difficulty-badge" style={{ 
                  backgroundColor: getDifficultyColor(company.difficulty_level) + '20',
                  color: getDifficultyColor(company.difficulty_level),
                  borderColor: getDifficultyColor(company.difficulty_level)
                }}>
                  {company.difficulty_level} Difficulty
                </span>
                <span className="hiring-badge">
                  <TrendingUp size={16} />
                  {company.hiring_frequency} Hiring
                </span>
                <span className="questions-badge">
                  <BookOpen size={16} />
                  {company.total_questions || questions.length} Questions
                </span>
              </div>
            </div>
          </div>
          {company.website && (
            <a href={company.website} target="_blank" rel="noopener noreferrer" className="company-website-btn">
              <ExternalLink size={18} />
              Visit Website
            </a>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-section">
        <div className="progress-info">
          <span>Your Progress</span>
          <span>{completedQuestions.size}/{questions.length} Questions ({progressPercentage}%)</span>
        </div>
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${progressPercentage}%` }}
          ></div>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs-container">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          <BookOpen size={18} />
          Overview
        </button>
        <button
          className={`tab ${activeTab === 'process' ? 'active' : ''}`}
          onClick={() => setActiveTab('process')}
        >
          <Target size={18} />
          Interview Process
        </button>
        <button
          className={`tab ${activeTab === 'questions' ? 'active' : ''}`}
          onClick={() => setActiveTab('questions')}
        >
          <FileText size={18} />
          Questions
        </button>
        <button
          className={`tab ${activeTab === 'strategy' ? 'active' : ''}`}
          onClick={() => setActiveTab('strategy')}
        >
          <Award size={18} />
          Strategy
        </button>
        <button
          className={`tab ${activeTab === 'resources' ? 'active' : ''}`}
          onClick={() => setActiveTab('resources')}
        >
          <Play size={18} />
          Resources
        </button>
        <button
          className={`tab ${activeTab === 'tips' ? 'active' : ''}`}
          onClick={() => setActiveTab('tips')}
        >
          <Lightbulb size={18} />
          Tips
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div className="overview-section">
            <div className="info-card">
              <h2>About {company.name}</h2>
              <p className="description">{company.description}</p>
              
              <div className="overview-grid">
                <div className="overview-item">
                  <div className="overview-icon" style={{ backgroundColor: '#6366f1' }}>
                    <Target size={24} />
                  </div>
                  <div>
                    <h4>Industry</h4>
                    <p>{company.industry || 'Technology'}</p>
                  </div>
                </div>
                
                <div className="overview-item">
                  <div className="overview-icon" style={{ backgroundColor: '#10b981' }}>
                    <TrendingUp size={24} />
                  </div>
                  <div>
                    <h4>Hiring Frequency</h4>
                    <p>{company.hiring_frequency}</p>
                  </div>
                </div>
                
                <div className="overview-item">
                  <div className="overview-icon" style={{ backgroundColor: '#f59e0b' }}>
                    <Star size={24} />
                  </div>
                  <div>
                    <h4>Difficulty Level</h4>
                    <p>{company.difficulty_level}</p>
                  </div>
                </div>
                
                <div className="overview-item">
                  <div className="overview-icon" style={{ backgroundColor: '#ef4444' }}>
                    <BookOpen size={24} />
                  </div>
                  <div>
                    <h4>Total Questions</h4>
                    <p>{company.total_questions || questions.length}</p>
                  </div>
                </div>
              </div>

              <div className="stats-grid">
                <div className="stat-box">
                  <div className="stat-number">{patterns.length}</div>
                  <div className="stat-label">Interview Rounds</div>
                </div>
                <div className="stat-box" style={{ background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)' }}>
                  <div className="stat-number">{questions.length}</div>
                  <div className="stat-label">Practice Questions</div>
                </div>
                <div className="stat-box" style={{ background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)' }}>
                  <div className="stat-number">{strategy?.total_weeks || 4}</div>
                  <div className="stat-label">Weeks Plan</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Interview Process Tab */}
        {activeTab === 'process' && (
          <div className="process-section">
            <h2>
              <Target size={28} />
              Interview Process
            </h2>
            <p className="section-subtitle">
              Complete interview rounds for {company.name}
            </p>
            
            <div className="process-timeline">
              {patterns.map((pattern, index) => (
                <div key={pattern.id} className="process-card">
                  <div className="process-step">
                    <div className="step-number">{index + 1}</div>
                    {index < patterns.length - 1 && <div className="step-line"></div>}
                  </div>
                  <div className="process-content">
                    <div className="process-header">
                      <h3>{pattern.round_name_display}</h3>
                      {pattern.duration && (
                        <span className="process-duration">
                          <Clock size={16} />
                          {pattern.duration}
                        </span>
                      )}
                    </div>
                    <p className="process-description">{pattern.description}</p>
                    <div className="process-tips">
                      <Lightbulb size={16} />
                      <strong>How to Crack:</strong>
                      <ul>
                        {pattern.round_name === 'Aptitude' && (
                          <>
                            <li>Practice quantitative aptitude daily</li>
                            <li>Focus on time management</li>
                            <li>Learn shortcut tricks for faster solving</li>
                          </>
                        )}
                        {pattern.round_name === 'Coding' && (
                          <>
                            <li>Practice DSA problems regularly</li>
                            <li>Focus on optimal solutions</li>
                            <li>Explain your approach clearly</li>
                          </>
                        )}
                        {pattern.round_name === 'Technical' && (
                          <>
                            <li>Revise core CS subjects thoroughly</li>
                            <li>Prepare your projects explanation</li>
                            <li>Practice problem-solving aloud</li>
                          </>
                        )}
                        {pattern.round_name === 'HR' && (
                          <>
                            <li>Research company values and culture</li>
                            <li>Prepare STAR method answers</li>
                            <li>Show enthusiasm and confidence</li>
                          </>
                        )}
                      </ul>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Questions Tab */}
        {activeTab === 'questions' && (
          <div className="questions-section">
            <div className="questions-header">
              <h2>
                <FileText size={28} />
                Practice Questions
              </h2>
              <div className="filter-buttons">
                <button
                  className={`filter-btn ${selectedQuestionType === 'all' ? 'active' : ''}`}
                  onClick={() => setSelectedQuestionType('all')}
                >
                  All ({questions.length})
                </button>
                {['HR', 'Technical', 'Coding', 'Aptitude'].map(type => (
                  <button
                    key={type}
                    className={`filter-btn ${selectedQuestionType === type ? 'active' : ''}`}
                    onClick={() => setSelectedQuestionType(type)}
                  >
                    {getTypeIcon(type)} {type}
                  </button>
                ))}
              </div>
            </div>

            <div className="questions-list">
              {questions
                .filter(q => selectedQuestionType === 'all' || q.question_type === selectedQuestionType)
                .map((q) => (
                <div key={q.id} className={`question-card ${completedQuestions.has(q.id) ? 'completed' : ''}`}>
                  <div className="question-header">
                    <div className="question-meta">
                      <span className="question-type-icon">{getTypeIcon(q.question_type)}</span>
                      <span className="question-type-badge">{q.question_type_display}</span>
                      <span 
                        className="question-difficulty"
                        style={{ backgroundColor: getDifficultyColor(q.difficulty) }}
                      >
                        {q.difficulty_display}
                      </span>
                    </div>
                    <div className="question-actions">
                      <button 
                        className={`complete-btn ${completedQuestions.has(q.id) ? 'done' : ''}`}
                        onClick={() => toggleQuestionComplete(q.id)}
                      >
                        {completedQuestions.has(q.id) ? (
                          <><CheckCircle size={16} /> Done</>
                        ) : (
                          <><Bookmark size={16} /> Mark Done</>
                        )}
                      </button>
                      <span className="expand-icon" onClick={() => toggleQuestion(q.id)}>
                        {expandedQuestions.has(q.id) ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
                      </span>
                    </div>
                  </div>
                  
                  <div className="question-text">
                    <HelpCircle size={20} />
                    <p>{q.question}</p>
                  </div>
                  
                  {expandedQuestions.has(q.id) && (
                    <div className="question-answer">
                      <div className="answer-section">
                        <strong>✅ Answer:</strong>
                        <p>{q.answer}</p>
                      </div>
                      
                      {q.youtube_link && (
                        <a href={q.youtube_link} target="_blank" rel="noopener noreferrer" className="youtube-link">
                          <Youtube size={20} />
                          Watch Video Explanation
                        </a>
                      )}
                      
                      {q.tags && (
                        <div className="question-tags">
                          <strong>Tags:</strong>
                          {q.tags.split(',').map((tag, i) => (
                            <span key={i} className="tag">{tag.trim()}</span>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Strategy Tab */}
        {activeTab === 'strategy' && strategy && (
          <div className="strategy-section">
            <h2>
              <Award size={28} />
              {strategy.total_weeks}-Week Preparation Strategy
            </h2>
            <p className="section-subtitle">
              Structured plan to crack {company.name} interview
            </p>

            <div className="strategy-timeline">
              {strategy.plan.map((week: any) => (
                <div key={week.week} className={`strategy-card ${completedWeeks.has(week.week) ? 'completed' : ''}`}>
                  <div className="strategy-header" onClick={() => toggleWeekComplete(week.week)}>
                    <div className="week-badge">
                      <div className={`week-check ${completedWeeks.has(week.week) ? 'checked' : ''}`}>
                        {completedWeeks.has(week.week) && <CheckCircle size={20} />}
                      </div>
                      <span>Week {week.week}</span>
                    </div>
                    <h3>{week.title}</h3>
                    <span className="hours-badge">
                      <Clock size={14} />
                      {week.hours_per_day} hrs/day
                    </span>
                  </div>
                  
                  <div className="strategy-tasks">
                    <ul>
                      {week.tasks.map((task: string, idx: number) => (
                        <li key={idx}>
                          <CheckCircle size={16} />
                          {task}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Resources Tab */}
        {activeTab === 'resources' && resources && (
          <div className="resources-section">
            <h2>
              <Play size={28} />
              Learning Resources
            </h2>
            <p className="section-subtitle">
              Curated resources to prepare for {company.name}
            </p>

            {/* YouTube Videos */}
            <div className="resource-category">
              <h3>
                <Youtube size={24} />
                YouTube Videos
              </h3>
              <div className="resources-grid">
                {resources.youtube.map((video: any, idx: number) => (
                  <div key={idx} className="resource-card">
                    <div className="resource-icon youtube-icon">
                      <Youtube size={32} />
                    </div>
                    <div className="resource-content">
                      <h4>{video.title}</h4>
                      <span className="resource-type">{video.type}</span>
                      <span className="resource-duration">{video.duration}</span>
                    </div>
                    <a href={video.url} target="_blank" rel="noopener noreferrer" className="resource-link">
                      <ExternalLink size={18} />
                      Watch
                    </a>
                  </div>
                ))}
              </div>
            </div>

            {/* Articles */}
            <div className="resource-category">
              <h3>
                <FileText size={24} />
                Articles & Guides
              </h3>
              <div className="resources-grid">
                {resources.articles.map((article: any, idx: number) => (
                  <div key={idx} className="resource-card">
                    <div className="resource-icon article-icon">
                      <FileText size={32} />
                    </div>
                    <div className="resource-content">
                      <h4>{article.title}</h4>
                      <span className="resource-type">{article.type}</span>
                      <span className="resource-duration">{article.read_time}</span>
                    </div>
                    <a href={article.url} target="_blank" rel="noopener noreferrer" className="resource-link">
                      <ExternalLink size={18} />
                      Read
                    </a>
                  </div>
                ))}
              </div>
            </div>

            {/* Courses */}
            <div className="resource-category">
              <h3>
                <BookOpen size={24} />
                Courses
              </h3>
              <div className="resources-grid">
                {resources.courses.map((course: any, idx: number) => (
                  <div key={idx} className="resource-card">
                    <div className="resource-icon course-icon">
                      <Award size={32} />
                    </div>
                    <div className="resource-content">
                      <h4>{course.title}</h4>
                      <span className="resource-type">{course.type}</span>
                      <span className="resource-price">{course.price}</span>
                    </div>
                    <a href={course.url} target="_blank" rel="noopener noreferrer" className="resource-link">
                      <ExternalLink size={18} />
                      Enroll
                    </a>
                  </div>
                ))}
              </div>
            </div>

            {/* Practice Platforms */}
            <div className="resource-category">
              <h3>
                <Code size={24} />
                Practice Platforms
              </h3>
              <div className="resources-grid">
                {resources.practice.map((platform: any, idx: number) => (
                  <div key={idx} className="resource-card">
                    <div className="resource-icon practice-icon">
                      <Code size={32} />
                    </div>
                    <div className="resource-content">
                      <h4>{platform.title}</h4>
                      <span className="resource-type">{platform.type}</span>
                      <span className="resource-problems">{platform.problems} Problems</span>
                    </div>
                    <a href={platform.url} target="_blank" rel="noopener noreferrer" className="resource-link">
                      <ExternalLink size={18} />
                      Practice
                    </a>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Tips Tab */}
        {activeTab === 'tips' && tips && (
          <div className="tips-section">
            <h2>
              <Lightbulb size={28} />
              Interview Tips & Advice
            </h2>
            <p className="section-subtitle">
              Essential tips to succeed in {company.name} interview
            </p>

            {/* Do's */}
            <div className="tips-category dos">
              <h3>
                <CheckCircle size={24} />
                Do's ✅
              </h3>
              <div className="tips-list">
                {tips.dos.map((tip: string, idx: number) => (
                  <div key={idx} className="tip-item">
                    <CheckCircle size={18} />
                    <p>{tip}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Don'ts */}
            <div className="tips-category donts">
              <h3>
                <AlertTriangle size={24} />
                Don'ts ❌
              </h3>
              <div className="tips-list">
                {tips.donts.map((tip: string, idx: number) => (
                  <div key={idx} className="tip-item">
                    <AlertTriangle size={18} />
                    <p>{tip}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Common Mistakes */}
            <div className="tips-category mistakes">
              <h3>
                <AlertTriangle size={24} />
                Common Mistakes to Avoid ⚠️
              </h3>
              <div className="tips-list">
                {tips.common_mistakes.map((mistake: string, idx: number) => (
                  <div key={idx} className="tip-item">
                    <span className="mistake-number">{idx + 1}</span>
                    <p>{mistake}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Success Tips */}
            <div className="tips-category success">
              <h3>
                <Star size={24} />
                Success Tips 🌟
              </h3>
              <div className="tips-list">
                {tips.success_tips.map((tip: string, idx: number) => (
                  <div key={idx} className="tip-item">
                    <Star size={18} />
                    <p>{tip}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CompanyDetail;
