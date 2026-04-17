import { useState, useEffect } from 'react';
import { Briefcase, Users, MessageSquare, ChevronDown, ChevronUp, Lightbulb, AlertCircle } from 'lucide-react';
import { hrgdService } from '../services/hrGdService';
import type { HRQuestion, GDTopic } from '../services/hrGdService';
import './HRGDPage.css';

const HRGDPage = () => {
  const [activeTab, setActiveTab] = useState<'hr' | 'gd'>('hr');
  const [hrQuestions, setHrQuestions] = useState<HRQuestion[]>([]);
  const [gdTopics, setGdTopics] = useState<GDTopic[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [expandedHr, setExpandedHr] = useState<number | null>(null);
  const [expandedGd, setExpandedGd] = useState<number | null>(null);

  useEffect(() => {
    loadHrQuestions();
    loadGdTopics();
  }, []);

  const loadHrQuestions = async () => {
    try {
      const data = await hrgdService.getHRQuestions();
      setHrQuestions(data);
    } catch (error) {
      console.error('Error loading HR questions:', error);
    }
  };

  const loadGdTopics = async () => {
    try {
      const data = await hrgdService.getGDTopics();
      setGdTopics(data);
    } catch (error) {
      console.error('Error loading GD topics:', error);
    }
  };

  const hrCategories = ['all', ...Array.from(new Set(hrQuestions.map(q => q.category)))];
  
  const filteredHrQuestions = selectedCategory === 'all' 
    ? hrQuestions 
    : hrQuestions.filter(q => q.category === selectedCategory);

  return (
    <div className="hrgd-page">
      <div className="hrgd-header">
        <h1>HR & Group Discussion Preparation</h1>
        <p>Master HR interviews and group discussions with comprehensive preparation material</p>
      </div>

      {/* Tab Selection */}
      <div className="hrgd-tabs">
        <button
          className={`tab ${activeTab === 'hr' ? 'active' : ''}`}
          onClick={() => setActiveTab('hr')}
        >
          <Briefcase size={20} />
          HR Interview Questions
        </button>
        <button
          className={`tab ${activeTab === 'gd' ? 'active' : ''}`}
          onClick={() => setActiveTab('gd')}
        >
          <Users size={20} />
          Group Discussion Topics
        </button>
      </div>

      {/* HR Questions Tab */}
      {activeTab === 'hr' && (
        <div className="hr-section">
          <div className="filter-bar">
            <MessageSquare size={20} />
            <span>Filter by Category:</span>
            <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}>
              {hrCategories.map(cat => (
                <option key={cat} value={cat}>
                  {cat === 'all' ? 'All Categories' : cat}
                </option>
              ))}
            </select>
          </div>

          <div className="hrgd-grid">
            {filteredHrQuestions.map((q) => (
              <div key={q.id} className="hrgd-card">
                <div className="card-header">
                  <span className={`category-badge ${q.category.toLowerCase().replace(' ', '-')}`}>
                    {q.category_display || q.category}
                  </span>
                  <button onClick={() => setExpandedHr(expandedHr === q.id ? null : q.id)}>
                    {expandedHr === q.id ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                  </button>
                </div>
                
                <h3 className="question-title">{q.question}</h3>
                
                {expandedHr === q.id && (
                  <div className="card-content">
                    <div className="sample-answer">
                      <div className="section-title">
                        <Lightbulb size={18} />
                        Sample Answer
                      </div>
                      <p>{q.sample_answer}</p>
                    </div>
                    
                    {q.tips && (
                      <div className="tips">
                        <div className="section-title">
                          <AlertCircle size={18} />
                          Tips
                        </div>
                        <p>{q.tips}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* GD Topics Tab */}
      {activeTab === 'gd' && (
        <div className="gd-section">
          <div className="hrgd-grid">
            {gdTopics.map((topic) => (
              <div key={topic.id} className="hrgd-card gd-card">
                <div className="card-header">
                  <span className={`category-badge ${topic.type.toLowerCase().replace(' ', '-')}`}>
                    {topic.type_display || topic.type}
                  </span>
                  <button onClick={() => setExpandedGd(expandedGd === topic.id ? null : topic.id)}>
                    {expandedGd === topic.id ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                  </button>
                </div>
                
                <h3 className="topic-title">{topic.topic}</h3>
                
                {expandedGd === topic.id && (
                  <div className="card-content">
                    <div className="gd-section intro">
                      <div className="section-title">Introduction Points</div>
                      <p>{topic.introduction_points}</p>
                    </div>
                    
                    <div className="gd-arguments">
                      <div className="argument for">
                        <div className="section-title">Arguments For</div>
                        <p>{topic.arguments_for}</p>
                      </div>
                      
                      {topic.arguments_against && (
                        <div className="argument against">
                          <div className="section-title">Arguments Against</div>
                          <p>{topic.arguments_against}</p>
                        </div>
                      )}
                    </div>
                    
                    <div className="gd-section dos-donts">
                      <div className="section-title">Do's and Don'ts</div>
                      <p>{topic.dos_and_donts}</p>
                    </div>
                    
                    {topic.conclusion_points && (
                      <div className="gd-section conclusion">
                        <div className="section-title">Conclusion</div>
                        <p>{topic.conclusion_points}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default HRGDPage;
