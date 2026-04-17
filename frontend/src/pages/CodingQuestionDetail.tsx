import { useState, useEffect } from'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Code2, Youtube, CheckCircle, Bookmark, PlayCircle, Lightbulb, Database } from'lucide-react';
import { codingService, type CodingQuestion } from '../services/codingService';
import './CodingQuestionDetail.css';

const CodingQuestionDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [question, setQuestion] = useState<CodingQuestion | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isSolved, setIsSolved] = useState(false);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);

  useEffect(() => {
    fetchQuestion();
  }, [id]);

  const fetchQuestion = async () => {
    try {
     setLoading(true);
      if (!id) return;
      
     const data = await codingService.getCodingQuestionById(parseInt(id));
     setQuestion(data);
     setIsSolved(data.is_solved);
     setIsBookmarked(data.is_bookmarked);
    } catch (err: any) {
     setError('Failed to load question details');
     console.error(err);
    } finally {
     setLoading(false);
    }
  };

  const handleMarkAsSolved = async () => {
    try {
      await codingService.markAsSolved(parseInt(id!));
     setIsSolved(true);
      alert('🎉 Problem marked as solved!');
    } catch (err: any) {
      alert('Please login to mark problems as solved');
    }
  };

  const handleBookmark = async () => {
    try {
      if (isBookmarked) {
        await codingService.removeBookmark(parseInt(id!));
       setIsBookmarked(false);
        alert('Bookmark removed');
      } else {
        await codingService.bookmarkQuestion(parseInt(id!));
       setIsBookmarked(true);
        alert('📑 Problem bookmarked!');
      }
    } catch (err: any) {
      alert('Please login to bookmark problems');
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return '#48bb78';
      case 'medium': return '#ed8936';
      case 'hard': return '#f56565';
     default: return '#4a5568';
    }
  };

  if (loading) {
   return (
      <div className="coding-detail-container">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading problem...</p>
        </div>
      </div>
    );
  }

  if (error || !question) {
   return (
      <div className="coding-detail-container">
        <div className="error-state">
          <h2>Error</h2>
          <p>{error || 'Question not found'}</p>
          <button onClick={() => navigate('/coding-practice')} className="back-button">
            Back to Problems
          </button>
        </div>
      </div>
    );
  }

 return (
    <div className="coding-detail-container">
      <div className="detail-header">
        <Link to="/coding-practice" className="back-button">
          <ArrowLeft size={20} />
          Back to Problems
        </Link>
        
        <div className="problem-header">
          <div className="problem-title-section">
            <Code2 size={40} className="problem-icon" />
            <h1>{question.title}</h1>
          </div>
          
          <div className="problem-actions">
            <button
              className={`action-btn ${isSolved ? 'solved' : ''}`}
              onClick={handleMarkAsSolved}
              disabled={isSolved}
            >
              <CheckCircle size={20} />
              {isSolved ? 'Solved' : 'Mark as Solved'}
            </button>
            
            <button
              className={`action-btn ${isBookmarked ? 'bookmarked' : ''}`}
              onClick={handleBookmark}
            >
              <Bookmark size={20} />
              {isBookmarked ? 'Bookmarked' : 'Bookmark'}
            </button>
          </div>
        </div>
        
        <div className="problem-meta">
          <span 
            className="difficulty-badge"
            style={{ backgroundColor: getDifficultyColor(question.difficulty) }}
          >
            {question.difficulty_display}
          </span>
          <span className="topic-badge">
            <Database size={16} />
            {question.topic_display}
          </span>
        </div>
      </div>

      <div className="problem-content">
        <div className="problem-description-card">
          <h2>Problem Description</h2>
          <p className="description-text">{question.description}</p>
          
          {question.constraints && (
            <div className="constraints-section">
              <h3>Constraints</h3>
              <pre className="constraints-text">{question.constraints}</pre>
            </div>
          )}
        </div>

        <div className="examples-card">
          <h2>Examples</h2>
          <div className="example-box">
            <div className="example-label">
              <PlayCircle size={16} />
              Sample Input
            </div>
            <pre className="example-code">{question.sample_input}</pre>
          </div>
          
          <div className="example-box">
            <div className="example-label">
              <CheckCircle size={16} />
              Sample Output
            </div>
            <pre className="example-code">{question.sample_output}</pre>
          </div>
        </div>

        <div className="explanation-section">
          <button
            className="toggle-explanation-btn"
            onClick={() => setShowExplanation(!showExplanation)}
          >
            <Lightbulb size={20} />
            {showExplanation ? 'Hide Explanation' : 'Show Explanation'}
          </button>
          
          {showExplanation && (
            <div className="explanation-content">
              <h3>Solution Approach</h3>
              <p className="explanation-text">{question.explanation}</p>
              
              {question.youtube_link && (
                <a 
                  href={question.youtube_link} 
                 target="_blank" 
                 rel="noopener noreferrer"
                  className="youtube-link"
                >
                  <Youtube size={20} />
                  Watch Video Solution
                </a>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CodingQuestionDetail;
