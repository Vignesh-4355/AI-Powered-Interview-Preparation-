import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Building2, TrendingUp, BookOpen, ArrowRight, Filter } from 'lucide-react';
import { companyService, type Company } from '../services/companyService';
import './CompanyList.css';

const CompanyList = () => {
  const navigate = useNavigate();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [filteredCompanies, setFilteredCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState<string>('all');

  useEffect(() => {
    fetchCompanies();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [searchQuery, difficultyFilter, companies]);

  const fetchCompanies = async () => {
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

  const applyFilters = () => {
    let filtered = [...companies];

    // Apply search filter
    if (searchQuery) {
      filtered = filtered.filter(
        (company) =>
          company.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          company.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
          company.industry.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Apply difficulty filter
    if (difficultyFilter !== 'all') {
      filtered = filtered.filter((company) => company.difficulty_level === difficultyFilter);
    }

    setFilteredCompanies(filtered);
  };

  const handleCompanyClick = (companyId: number) => {
    navigate(`/company/${companyId}`);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy':
        return '#10b981';
      case 'Medium':
        return '#f59e0b';
      case 'Hard':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };

  const getHiringBadgeColor = (frequency: string) => {
    switch (frequency) {
      case 'High':
        return 'rgba(16, 185, 129, 0.1)';
      case 'Medium':
        return 'rgba(245, 158, 11, 0.1)';
      case 'Low':
        return 'rgba(239, 68, 68, 0.1)';
      default:
        return 'rgba(107, 114, 128, 0.1)';
    }
  };

  return (
    <div className="company-list-page">
      {/* Hero Section */}
      <div className="company-list-header">
        <h1>
          <Building2 size={36} />
          Choose Your Target Company
        </h1>
        <p>Select a company to access tailored interview preparation with company-specific questions and patterns</p>
      </div>

      {/* Search & Filter Bar */}
      <div className="company-filters">
        <div className="search-box">
          <Search size={20} />
          <input
            type="text"
            placeholder="Search companies by name or industry..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="filter-box">
          <Filter size={18} />
          <select
            value={difficultyFilter}
            onChange={(e) => setDifficultyFilter(e.target.value)}
          >
            <option value="all">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
      </div>

      {/* Results Count */}
      <div className="results-info">
        <span>{filteredCompanies.length} compan{filteredCompanies.length === 1 ? 'y' : 'ies'} found</span>
      </div>

      {/* Companies Grid */}
      {loading ? (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading companies...</p>
        </div>
      ) : error ? (
        <div className="error-container">
          <p>{error}</p>
          <button onClick={fetchCompanies}>Retry</button>
        </div>
      ) : filteredCompanies.length === 0 ? (
        <div className="empty-container">
          <Building2 size={64} />
          <h3>No companies found</h3>
          <p>Try adjusting your search or filter criteria</p>
        </div>
      ) : (
        <div className="companies-grid">
          {filteredCompanies.map((company) => (
            <div
              key={company.id}
              className="company-card"
              onClick={() => handleCompanyClick(company.id)}
            >
              <div className="company-card-header">
                <div className="company-logo">
                  {company.logo ? (
                    <img src={company.logo} alt={company.name} />
                  ) : (
                    <Building2 size={40} />
                  )}
                </div>
                <div className="company-badges">
                  <span
                    className="difficulty-badge"
                    style={{
                      backgroundColor: getDifficultyColor(company.difficulty_level) + '20',
                      color: getDifficultyColor(company.difficulty_level),
                      borderColor: getDifficultyColor(company.difficulty_level),
                    }}
                  >
                    {company.difficulty_level}
                  </span>
                </div>
              </div>

              <div className="company-card-body">
                <h3>{company.name}</h3>
                <p className="company-industry">{company.industry}</p>
                <p className="company-description">{company.description}</p>
              </div>

              <div className="company-card-footer">
                <div className="company-stats">
                  <div className="stat">
                    <BookOpen size={16} />
                    <span>{company.total_questions} Questions</span>
                  </div>
                  <div className="stat" style={{ backgroundColor: getHiringBadgeColor(company.hiring_frequency) }}>
                    <TrendingUp size={16} />
                    <span>{company.hiring_frequency} Hiring</span>
                  </div>
                </div>
                <button className="prepare-btn">
                  Prepare Now
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CompanyList;
