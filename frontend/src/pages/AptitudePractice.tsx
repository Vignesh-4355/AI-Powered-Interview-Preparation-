import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, CheckCircle, XCircle, Clock, Play, 
  Youtube, ChevronRight, ChevronLeft, Lightbulb,
  RotateCcw, Award, Timer
} from 'lucide-react';
import { aptitudeService, type AptitudeQuestionList } from '../services/aptitudeService';
import './AptitudePractice.css';

const AptitudePractice = () => {
  const { category } = useParams<{ category: string }>();
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<AptitudeQuestionList[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [timer, setTimer] = useState(0);
  const [isTimerRunning, setIsTimerRunning] = useState(false);
  const [score, setScore] = useState({ correct: 0, attempted: 0 });
  const [wrongAnswers, setWrongAnswers] = useState<number[]>([]);

  const decodedCategory = decodeURIComponent(category || '');

  useEffect(() => {
    fetchQuestions();
  }, [category]);

  useEffect(() => {
    let interval: number | undefined;
    if (isTimerRunning && !submitted) {
      interval = setInterval(() => {
        setTimer(prev => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isTimerRunning, submitted]);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      const data = await aptitudeService.getQuestionsByCategory(decodedCategory);
      setQuestions(data);
      setCurrentIndex(0);
      resetQuestion();
    } catch (err) {
      console.error('Failed to fetch questions:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetQuestion = () => {
    setSelectedAnswer('');
    setSubmitted(false);
    setResult(null);
    setTimer(0);
    setIsTimerRunning(true);
  };

  const handleSubmit = useCallback(async () => {
    if (!selectedAnswer || questions.length === 0) return;

    setIsTimerRunning(false);
    const currentQuestion = questions[currentIndex];

    try {
      const data = await aptitudeService.submitAnswer(currentQuestion.id, selectedAnswer, timer);
      setResult(data);
      setSubmitted(true);
      setScore(prev => ({
        correct: prev.correct + (data.is_correct ? 1 : 0),
        attempted: prev.attempted + 1
      }));

      if (!data.is_correct) {
        setWrongAnswers(prev => [...prev, currentIndex]);
      }
    } catch (err) {
      console.error('Failed to submit answer:', err);
    }
  }, [selectedAnswer, questions, currentIndex, timer]);

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(prev => prev + 1);
      resetQuestion();
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
      resetQuestion();
    }
  };

  const handleRetryWrong = () => {
    if (wrongAnswers.length > 0) {
      const wrongQuestions = wrongAnswers.map(idx => questions[idx]);
      setQuestions(wrongQuestions);
      setCurrentIndex(0);
      setWrongAnswers([]);
      setScore({ correct: 0, attempted: 0 });
      resetQuestion();
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getAccuracy = () => {
    if (score.attempted === 0) return 0;
    return Math.round((score.correct / score.attempted) * 100);
  };

  if (loading) {
    return (
      <div className="aptitude-practice-loading">
        <div className="spinner" />
        <p>Loading questions...</p>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="aptitude-practice-empty">
        <h2>No Questions Available</h2>
        <p>Check back later for questions in this category.</p>
        <button onClick={() => navigate('/aptitude')} className="back-btn">
          <ArrowLeft size={18} />
          Back to Categories
        </button>
      </div>
    );
  }

  const currentQuestion = questions[currentIndex];
  const progress = ((currentIndex + 1) / questions.length) * 100;

  return (
    <div className="aptitude-practice-page">
      {/* Header */}
      <div className="practice-header">
        <button onClick={() => navigate('/aptitude')} className="back-button">
          <ArrowLeft size={20} />
          Back
        </button>
        <div className="practice-info">
          <h2>{decodedCategory}</h2>
          <div className="practice-stats">
            <div className="stat">
              <Award size={18} />
              <span>Score: {score.correct}/{score.attempted}</span>
            </div>
            <div className="stat">
              <Timer size={18} />
              <span>Accuracy: {getAccuracy()}%</span>
            </div>
          </div>
        </div>
        <div className="timer-display">
          <Clock size={20} />
          <span>{formatTime(timer)}</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-container">
        <div className="progress-info">
          <span>Question {currentIndex + 1} of {questions.length}</span>
          <span>{Math.round(progress)}% Complete</span>
        </div>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>
      </div>

      {/* Question Card */}
      <div className="question-card">
        <div className="question-header">
          <span className={`difficulty-badge ${currentQuestion.difficulty.toLowerCase()}`}>
            {currentQuestion.difficulty}
          </span>
          <span className="question-number">Q{currentIndex + 1}</span>
        </div>

        <div className="question-text">
          {currentQuestion.question}
        </div>

        {/* Options */}
        <div className="options-container">
          {currentQuestion.options.map((option, index) => {
            const isCorrect = submitted && option === result.correct_answer;
            const isWrong = submitted && option === selectedAnswer && !result.is_correct;
            
            return (
              <div
                key={index}
                className={`option ${
                  submitted 
                    ? isCorrect 
                      ? 'correct' 
                      : isWrong 
                        ? 'wrong' 
                        : ''
                    : selectedAnswer === option 
                      ? 'selected' 
                      : ''
                }`}
                onClick={() => !submitted && setSelectedAnswer(option)}
              >
                <div className="option-radio">
                  {submitted && isCorrect && <CheckCircle size={20} />}
                  {submitted && isWrong && <XCircle size={20} />}
                  {!submitted && selectedAnswer === option && <div className="radio-selected" />}
                </div>
                <span className="option-text">{option}</span>
              </div>
            );
          })}
        </div>

        {/* Action Buttons */}
        {!submitted ? (
          <button
            className="submit-btn"
            onClick={handleSubmit}
            disabled={!selectedAnswer}
          >
            <Play size={20} />
            Submit Answer
          </button>
        ) : (
          <div className="result-section">
            {/* Result Message */}
            <div className={`result-message ${result.is_correct ? 'correct' : 'incorrect'}`}>
              {result.is_correct ? (
                <>
                  <CheckCircle size={24} />
                  <div>
                    <h3>Correct! 🎉</h3>
                    <p>Great job! You got it right.</p>
                  </div>
                </>
              ) : (
                <>
                  <XCircle size={24} />
                  <div>
                    <h3>Incorrect</h3>
                    <p>The correct answer is: <strong>{result.correct_answer}</strong></p>
                  </div>
                </>
              )}
            </div>

            {/* Solution */}
            <div className="solution-section">
              <h3>
                <Lightbulb size={20} />
                Step-by-Step Solution
              </h3>
              <div className="solution-content">
                {result.solution?.split('\n').map((line: string, idx: number) => (
                  <p key={idx}>{line}</p>
                ))}
              </div>
            </div>

            {/* Explanation */}
            <div className="explanation-section">
              <h3>
                <Lightbulb size={20} />
                Explanation
              </h3>
              <p>{result.explanation}</p>
            </div>

            {/* Formula */}
            {result.formula_used && (
              <div className="formula-section">
                <h3>📐 Formula Used</h3>
                <p className="formula">{result.formula_used}</p>
              </div>
            )}

            {/* YouTube Link */}
            {result.youtube_link && (
              <a
                href={result.youtube_link}
                target="_blank"
                rel="noopener noreferrer"
                className="youtube-link"
              >
                <Youtube size={20} />
                Watch Video Explanation
              </a>
            )}

            {/* Navigation */}
            <div className="navigation-buttons">
              <button
                className="nav-btn"
                onClick={handlePrevious}
                disabled={currentIndex === 0}
              >
                <ChevronLeft size={18} />
                Previous
              </button>

              {wrongAnswers.length > 0 && currentIndex === questions.length - 1 && (
                <button className="retry-btn" onClick={handleRetryWrong}>
                  <RotateCcw size={18} />
                  Retry Wrong ({wrongAnswers.length})
                </button>
              )}

              {currentIndex < questions.length - 1 ? (
                <button className="nav-btn primary" onClick={handleNext}>
                  Next
                  <ChevronRight size={18} />
                </button>
              ) : (
                <div className="completion-message">
                  <Award size={24} />
                  <p>Practice Complete! Accuracy: {getAccuracy()}%</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AptitudePractice;
