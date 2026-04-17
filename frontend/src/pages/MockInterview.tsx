import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Video, Play, Award, Clock, CheckCircle,
  ArrowRight, RotateCcw, BarChart3, FileText
} from 'lucide-react';
import { mockInterviewService, type InterviewQuestion, type MockInterviewSession } from '../services/mockInterviewService';
import './MockInterview.css';

const MockInterview = () => {
  const navigate = useNavigate();
  const [mode, setMode] = useState<'setup' | 'interview' | 'result'>('setup');
  
  // Setup state
  const [interviewType, setInterviewType] = useState<'HR' | 'Technical' | 'Coding' | 'Mixed'>('Mixed');
  const [difficulty, setDifficulty] = useState<'Easy' | 'Medium' | 'Hard'>('Medium');
  const [totalQuestions, setTotalQuestions] = useState(5);
  
  // Interview state
  const [session, setSession] = useState<MockInterviewSession | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<InterviewQuestion | null>(null);
  const [questionNumber, setQuestionNumber] = useState(1);
  const [answerText, setAnswerText] = useState('');
  // const [answers, setAnswers] = useState<UserAnswer[]>([]);
  const [previousFeedback, setPreviousFeedback] = useState('');
  const [loading, setLoading] = useState(false);
  const [timer, setTimer] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    let interval: number | undefined;
    if (mode === 'interview' && !isCompleted) {
      interval = setInterval(() => setTimer(prev => prev + 1), 1000);
    }
    return () => clearInterval(interval);
  }, [mode, isCompleted]);

  const handleStartInterview = async () => {
    setLoading(true);
    try {
      const data = await mockInterviewService.startInterview({
        interview_type: interviewType,
        difficulty,
        total_questions: totalQuestions,
      });
      setSession(data.session);
      setCurrentQuestion(data.question);
      setQuestionNumber(data.question_number);
      setMode('interview');
      setTimer(0);
    } catch (err) {
      console.error('Failed to start interview:', err);
      alert('Failed to start interview. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!answerText.trim() || !session || !currentQuestion) return;

    setLoading(true);
    try {
      const data = await mockInterviewService.submitAnswer({
        session_id: session.id,
        question_id: currentQuestion.id,
        answer_text: answerText,
      });

      if (data.completed && data.session) {
        // Interview completed
        setSession(data.session);
        setIsCompleted(true);
        setMode('result');
      } else if (data.question) {
        // More questions
        setCurrentQuestion(data.question);
        setQuestionNumber(data.question_number || questionNumber + 1);
        setPreviousFeedback(data.previous_feedback || '');
        setAnswerText('');
      }
    } catch (err) {
      console.error('Failed to submit answer:', err);
      alert('Failed to submit answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getScoreColor = (score: number | null) => {
    if (!score) return '#94a3b8';
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  };

  // Setup Page
  if (mode === 'setup') {
    return (
      <div className="mock-interview-page">
        <div className="interview-setup">
          <div className="setup-header">
            <Video size={48} />
            <h1>Mock Interview Simulator</h1>
            <p>Practice real interview scenarios with AI-powered feedback</p>
          </div>

          <div className="setup-form">
            <div className="form-group">
              <label>Interview Type</label>
              <div className="option-grid">
                {(['HR', 'Technical', 'Coding', 'Mixed'] as const).map((type) => (
                  <button
                    key={type}
                    className={`option-btn ${interviewType === type ? 'active' : ''}`}
                    onClick={() => setInterviewType(type)}
                  >
                    {type}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label>Difficulty Level</label>
              <div className="option-grid">
                {(['Easy', 'Medium', 'Hard'] as const).map((level) => (
                  <button
                    key={level}
                    className={`option-btn ${difficulty === level ? 'active' : ''}`}
                    onClick={() => setDifficulty(level)}
                  >
                    {level}
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label>Number of Questions</label>
              <div className="option-grid">
                {[3, 5, 10].map((num) => (
                  <button
                    key={num}
                    className={`option-btn ${totalQuestions === num ? 'active' : ''}`}
                    onClick={() => setTotalQuestions(num)}
                  >
                    {num} Questions
                  </button>
                ))}
              </div>
            </div>

            <button className="start-btn" onClick={handleStartInterview} disabled={loading}>
              <Play size={20} />
              {loading ? 'Starting...' : 'Start Interview'}
            </button>
          </div>

          <div className="interview-guidelines">
            <h3>
              <FileText size={20} />
              Interview Guidelines
            </h3>
            <ul>
              <li>Read each question carefully before answering</li>
              <li>Provide detailed, structured responses</li>
              <li>Use specific examples and technical terms</li>
              <li>Take your time - there's a timer but no time limit</li>
              <li>You'll receive feedback after each answer</li>
              <li>Final score based on keyword matching and completeness</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  // Interview Session Page
  if (mode === 'interview' && currentQuestion && session) {
    const progress = (questionNumber / session.total_questions) * 100;

    return (
      <div className="mock-interview-page">
        <div className="interview-session">
          {/* Header */}
          <div className="session-header">
            <div className="session-info">
              <h2>{session.interview_type_display} Interview</h2>
              <div className="session-meta">
                <span className="meta-item">
                  <Clock size={16} />
                  {formatTime(timer)}
                </span>
                <span className="meta-item">
                  <Award size={16} />
                  {session.difficulty_display}
                </span>
              </div>
            </div>
            <div className="progress-info">
              <span>Question {questionNumber} of {session.total_questions}</span>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>

          {/* Previous Feedback */}
          {previousFeedback && (
            <div className="feedback-banner">
              <BarChart3 size={20} />
              <p>{previousFeedback}</p>
            </div>
          )}

          {/* Question */}
          <div className="question-card">
            <div className="question-header">
              <span className={`type-badge ${currentQuestion.question_type.toLowerCase()}`}>
                {currentQuestion.question_type_display}
              </span>
              <span className={`difficulty-badge ${currentQuestion.difficulty.toLowerCase()}`}>
                {currentQuestion.difficulty_display}
              </span>
            </div>
            <div className="question-text">
              {currentQuestion.question_text}
            </div>
          </div>

          {/* Answer Input */}
          <div className="answer-section">
            <label>Your Answer</label>
            <textarea
              value={answerText}
              onChange={(e) => setAnswerText(e.target.value)}
              placeholder="Type your detailed answer here... Include specific examples and technical terms."
              rows={10}
              disabled={loading}
            />
            <div className="answer-actions">
              <button
                className="submit-answer-btn"
                onClick={handleSubmitAnswer}
                disabled={!answerText.trim() || loading}
              >
                {loading ? 'Submitting...' : questionNumber < session.total_questions ? 'Submit & Next' : 'Submit & Complete'}
                <ArrowRight size={18} />
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Result Page
  if (mode === 'result' && session) {
    return (
      <div className="mock-interview-page">
        <div className="interview-result">
          <div className="result-header">
            <CheckCircle size={64} />
            <h1>Interview Complete!</h1>
            <p>Here's your performance summary</p>
          </div>

          {/* Score Card */}
          <div className="score-card">
            <div className="score-circle" style={{ borderColor: getScoreColor(session.score) }}>
              <div className="score-value" style={{ color: getScoreColor(session.score) }}>
                {session.score?.toFixed(1) || 'N/A'}
              </div>
              <div className="score-label">Overall Score</div>
            </div>
            <div className="score-details">
              <div className="detail-item">
                <span className="label">Questions Answered</span>
                <span className="value">{session.answers?.length || 0}/{session.total_questions}</span>
              </div>
              <div className="detail-item">
                <span className="label">Time Taken</span>
                <span className="value">{formatTime(timer)}</span>
              </div>
              <div className="detail-item">
                <span className="label">Interview Type</span>
                <span className="value">{session.interview_type_display}</span>
              </div>
              <div className="detail-item">
                <span className="label">Difficulty</span>
                <span className="value">{session.difficulty_display}</span>
              </div>
            </div>
          </div>

          {/* Feedback */}
          {session.feedback && (
            <div className="feedback-section">
              <h3>
                <BarChart3 size={20} />
                AI Feedback
              </h3>
              <p>{session.feedback}</p>
            </div>
          )}

          {/* Answers Review */}
          <div className="answers-review">
            <h3>Detailed Answers</h3>
            {session.answers?.map((answer, index) => (
              <div key={answer.id} className="answer-card">
                <div className="answer-header">
                  <span className="answer-number">Q{index + 1}</span>
                  <span className="answer-score" style={{ color: getScoreColor(answer.keyword_score) }}>
                    Score: {answer.keyword_score.toFixed(1)}/100
                  </span>
                </div>
                <div className="answer-question">{answer.question_text}</div>
                <div className="answer-text">
                  <strong>Your Answer:</strong>
                  <p>{answer.answer_text}</p>
                </div>
                {answer.feedback && (
                  <div className="answer-feedback">
                    <strong>Feedback:</strong>
                    <p>{answer.feedback}</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Action Buttons */}
          <div className="result-actions">
            <button className="action-btn primary" onClick={() => navigate('/mock-interview')}>
              <RotateCcw size={18} />
              Take Another Interview
            </button>
            <button className="action-btn secondary" onClick={() => navigate('/dashboard')}>
              Back to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default MockInterview;
