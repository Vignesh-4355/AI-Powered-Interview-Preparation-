import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, ArrowLeft, Building2, TrendingUp, Award, BookOpen, Filter } from 'lucide-react';
import { companyService, type Company } from '../services/companyService';
import './CompanySelection.css';

const CompanySelection = () => {
  const navigate = useNavigate();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState('');

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      setLoading(true);
      const data = await companyService.getAllCompanies();
      setCompanies(data);
    } catch (err) {
      setError('Failed to load companies');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredCompanies = companies.filter((company) => {
    const matchesSearch =
      company.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      company.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      company.industry?.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesDifficulty =
      !difficultyFilter || company.difficulty_level === difficultyFilter;

    return matchesSearch && matchesDifficulty;
  });

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy': return '#22c55e';
      case 'Medium': return '#f59e0b';
      case 'Hard': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const getHiringBadge = (frequency: string) => {
    switch (frequency) {
      case 'High':
        return { icon: <TrendingUp size={14} />, label: 'High Hiring', color: '#22c55e' };
      case 'Medium':
        return { icon: <BookOpen size={14} />, label: 'Medium Hiring', color: '#f59e0b' };
      case 'Low':
        return { icon: <Award size={14} />, label: 'Selective', color: '#8b5cf6' };
      default:
        return { icon: <BookOpen size={14} />, label: 'Medium', color: '#6b7280' };
    }
  };

  const handleCompanyClick = (companyId: number) => {
    navigate(`/company/${companyId}`);
  };

  return (
    <div className="company-selection-page">
      {/* Header Section */}
      <div className="cs-header">
        <button className="cs-back-btn" onClick={() => navigate('/dashboard')}>
          <ArrowLeft size={20} />
          <span>Back to Dashboard</span>
        </button>
        
        <div className="cs-title-section">
          <div className="cs-icon-large">
            <Building2 size={56} />
          </div>
          <h1>Choose Your Target Company</h1>
          <p>Select a company to access tailored interview questions, patterns, and preparation strategies</p>
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="cs-controls">
        <div className="cs-search-box">
          <Search size={20} className="cs-search-icon" />
          <input
            type="text"
            placeholder="Search companies by name, industry, or description..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="cs-search-input"
          />
          {searchQuery && (
            <button
              className="cs-search-clear"
              onClick={() => setSearchQuery('')}
            >
              ×
            </button>
          )}
        </div>

        <div className="cs-filter-group">
          <Filter size={18} />
          <select
            value={difficultyFilter}
            onChange={(e) => setDifficultyFilter(e.target.value)}
            className="cs-filter-select"
          >
            <option value="">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
      </div>

      {/* Results Count */}
      <div className="cs-results-count">
        <span className="cs-count-badge">{filteredCompanies.length}</span>
        <span>companies found</span>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="cs-loading">
          <div className="cs-spinner"></div>
          <p>Loading companies...</p>
        </div>
      )}

      {/* Error State */}
      {error && <div className="cs-error">{error}</div>}

      {/* Empty State */}
      {!loading && filteredCompanies.length === 0 && (
        <div className="cs-empty">
          <Search size={64} />
          <h3>No companies found</h3>
          <p>Try adjusting your search or filter criteria</p>
          <button onClick={() => { setSearchQuery(''); setDifficultyFilter(''); }}>
            Clear Filters
          </button>
        </div>
      )}

      {/* Companies Grid */}
      {!loading && filteredCompanies.length > 0 && (
        <div className="cs-grid">
          {filteredCompanies.map((company) => {
            const hiringInfo = getHiringBadge(company.hiring_frequency || 'Medium');
            
            return (
              <div
                key={company.id}
                className="cs-company-card"
                onClick={() => handleCompanyClick(company.id)}
              >
                {/* Card Header with Logo */}
                <div className="cs-card-header">
                  {company.logo ? (
                    <img
                      src={company.logo}
                      alt={company.name}
                      className="cs-company-logo"
                      onError={(e) => {
                        (e.target as HTMLImageElement).style.display = 'none';
                        (e.target as HTMLImageElement).nextElementSibling?.classList.add('visible');
                      }}
                    />
                  ) : null}
                  <div className={`cs-logo-fallback ${!company.logo ? 'visible' : ''}`}>
                    <Building2 size={32} />
                  </div>
                  
                  <div className="cs-card-badges">
                    <span
                      className="cs-difficulty-badge"
                      style={{ backgroundColor: getDifficultyColor(company.difficulty_level || 'Medium') }}
                    >
                      {company.difficulty_level || 'Medium'}
                    </span>
                    <span
                      className="cs-hiring-badge"
                      style={{ color: hiringInfo.color }}
                    >
                      {hiringInfo.icon}
                      <span>{hiringInfo.label}</span>
                    </span>
                  </div>
                </div>

                {/* Card Content */}
                <div className="cs-card-content">
                  <h2 className="cs-company-name">{company.name}</h2>
                  {company.industry && (
                    <p className="cs-company-industry">{company.industry}</p>
                  )}
                  <p className="cs-company-description">
                    {company.description?.substring(0, 120)}
                    {(company.description?.length || 0) > 120 ? '...' : ''}
                  </p>

                  {/* Stats */}
                  <div className="cs-company-stats">
                    <div className="cs-stat">
                      <BookOpen size={16} />
                      <span>{company.total_questions || 0} Questions</span>
                    </div>
                  </div>
                </div>

                {/* Card Footer */}
                <div className="cs-card-footer">
                  <button className="cs-prepare-btn">
                    <span>Prepare Now</span>
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                      <path d="M7.5 15L12.5 10L7.5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default CompanySelection;
