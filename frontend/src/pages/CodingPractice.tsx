import { useState, useEffect } from'react';
import { Link, useNavigate } from'react-router-dom';
import { ArrowLeft, Code2, Search, Filter, Bookmark, CheckCircle } from 'lucide-react';
import { codingService, type CodingQuestion } from '../services/codingService';
import './CodingPractice.css';

const CodingPractice = () => {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<CodingQuestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('all');
  const [filteredQuestions, setFilteredQuestions] = useState<CodingQuestion[]>([]);

  useEffect(() => {
    fetchQuestions();
  }, []);

  useEffect(() => {
    filterQuestions();
  }, [searchQuery, selectedDifficulty, questions]);

  const fetchQuestions = async () => {
   try {
    setLoading(true);
    const data = await codingService.getCodingQuestions();
    setQuestions(data);
    setFilteredQuestions(data);
   } catch (err: any) {
    console.error(err);
   } finally {
    setLoading(false);
   }
 };

  const filterQuestions = () => {
   let filtered = [...questions];

    if (searchQuery.trim()) {
     filtered = filtered.filter(q => 
      q.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
       q.topic_display?.toLowerCase().includes(searchQuery.toLowerCase())
     );
   }

    if (selectedDifficulty !== 'all') {
     filtered = filtered.filter(q => q.difficulty === selectedDifficulty);
   }

  setFilteredQuestions(filtered);
 };

  const handleQuestionClick = (questionId: number) => {
   navigate(`/coding-practice/${questionId}`);
 };

  const getDifficultyBadgeClass = (difficulty: string) => {
   switch (difficulty.toLowerCase()) {
     case 'easy': return 'difficulty-easy';
     case 'medium': return 'difficulty-medium';
     case 'hard': return 'difficulty-hard';
    default: return '';
   }
 };

  if (loading) {
  return (
     <div className="coding-practice-container">
       <div className="loading-state">
         <div className="spinner"></div>
         <p>Loading coding questions...</p>
       </div>
     </div>
   );
 }

 return (
   <div className="coding-practice-container">
     <div className="prep-header">
       <Link to="/dashboard" className="back-button">
         <ArrowLeft size={20} />
         Back to Dashboard
       </Link>
       
       <div className="header-content">
         <Code2 size={48} className="header-icon" />
         <h1>Coding Practice</h1>
         <p className="subtitle">
           Master data structures and algorithms with hands-on coding problems
         </p>
       </div>
     </div>

     <div className="filters-section">
       <div className="search-box">
         <Search size={20} className="search-icon" />
         <input
           type="text"
           placeholder="Search problems by title or topic..."
           value={searchQuery}
           onChange={(e) => setSearchQuery(e.target.value)}
           className="search-input"
         />
       </div>

       <div className="filter-buttons">
         <Filter size={18} />
         <span className="filter-label">Difficulty:</span>
         <button
           className={`filter-btn ${selectedDifficulty === 'all' ? 'active' : ''}`}
           onClick={() => setSelectedDifficulty('all')}
         >
           All
         </button>
         <button
           className={`filter-btn difficulty-easy ${selectedDifficulty === 'Easy' ? 'active' : ''}`}
           onClick={() => setSelectedDifficulty('Easy')}
         >
           Easy
         </button>
         <button
           className={`filter-btn difficulty-medium ${selectedDifficulty === 'Medium' ? 'active' : ''}`}
           onClick={() => setSelectedDifficulty('Medium')}
         >
           Medium
         </button>
         <button
           className={`filter-btn difficulty-hard ${selectedDifficulty === 'Hard' ? 'active' : ''}`}
           onClick={() => setSelectedDifficulty('Hard')}
         >
           Hard
         </button>
       </div>
     </div>

     <div className="questions-stats">
       <p>Showing {filteredQuestions.length} of {questions.length} problems</p>
     </div>

     <div className="questions-grid">
       {filteredQuestions.length === 0 ? (
         <div className="no-results">
           <p>No coding questions found</p>
         </div>
       ) : (
         filteredQuestions.map((question) => (
           <div
             key={question.id}
             className="question-card"
             onClick={() => handleQuestionClick(question.id)}
           >
             <div className="question-card-header">
               <h3 className="question-title">{question.title}</h3>
               <div className="question-status">
                 {question.is_solved && (
                   <CheckCircle size={20} className="solved-icon" />
                 )}
                 {question.is_bookmarked && (
                   <Bookmark size={20} className="bookmarked-icon" />
                 )}
               </div>
             </div>

             <div className="question-card-body">
               <div className="question-meta">
                 <span className={`difficulty-badge ${getDifficultyBadgeClass(question.difficulty)}`}>
                   {question.difficulty_display}
                 </span>
                 <span className="topic-tag">{question.topic_display}</span>
               </div>
             </div>

             <div className="question-card-footer">
               <span className="view-problem-btn">View Problem →</span>
             </div>
           </div>
         ))
       )}
     </div>
   </div>
 );
};

export default CodingPractice;
