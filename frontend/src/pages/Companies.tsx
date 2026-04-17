import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Building2, ArrowLeft, Search, ExternalLink, MapPin, Users, Award } from 'lucide-react';
import { companyService, type Company } from '../services/companyService';
import './ModulePage.css';

const Companies = () => {
  const navigate = useNavigate();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredCompanies, setFilteredCompanies] = useState<Company[]>([]);

  useEffect(() => {
    fetchCompanies();
  }, []);

  useEffect(() => {
    if (searchQuery.trim()) {
      const filtered = companies.filter(company =>
        company.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        company.industry?.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredCompanies(filtered);
    } else {
      setFilteredCompanies(companies);
    }
  }, [searchQuery, companies]);

  const fetchCompanies = async () => {
    try {
      setLoading(true);
      const data = await companyService.getAllCompanies();
      setCompanies(data);
      setFilteredCompanies(data);
    } catch (error) {
      console.error('Failed to fetch companies:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCompanyClick = (companyId: number) => {
    navigate(`/companies/${companyId}`);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy': return '#10b981';
      case 'Medium': return '#f59e0b';
      case 'Hard': return '#ef4444';
      default: return '#6b7280';
    }
  };

  if (loading) {
    return (
      <div className="module-page-container">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading companies...</p>
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
          <Building2 size={64} />
        </div>
        <h1>Company Specific Preparation</h1>
        <p className="module-subtitle">
          Explore top tech companies and their interview processes. Get company-specific questions and preparation strategies.
        </p>
      </div>

      <div className="module-content">
        {/* Search Bar */}
        <div className="search-section">
          <Search size={20} className="search-icon" />
          <input
            type="text"
            placeholder="Search companies by name or industry..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </div>

        {/* Stats */}
        <div className="companies-stats">
          <div className="stat-badge">
            <span className="stat-number">{filteredCompanies.length}</span>
            <span className="stat-label">Companies</span>
          </div>
        </div>

        {/* Companies Grid */}
        <div className="companies-grid">
          {filteredCompanies.length === 0 ? (
            <div className="no-results">
              <Building2 size={48} />
              <p>No companies found</p>
            </div>
          ) : (
            filteredCompanies.map((company) => (
              <div
                key={company.id}
                className="company-card"
                onClick={() => handleCompanyClick(company.id)}
              >
                <div className="company-card-header">
                  <div className="company-logo-wrapper">
                    {company.logo ? (
                      <img src={company.logo} alt={company.name} className="company-logo" />
                    ) : (
                      <div className="company-logo-placeholder">
                        <Building2 size={32} />
                      </div>
                    )}
                  </div>
                  <div className="company-info">
                    <h3 className="company-name">{company.name}</h3>
                    <div className="company-industry">
                      <MapPin size={14} />
                      {company.industry}
                    </div>
                  </div>
                </div>

                <div className="company-card-body">
                  <p className="company-description">
                    {company.description?.substring(0, 120)}...
                  </p>

                  <div className="company-tags">
                    <div className="tag difficulty-tag" style={{ background: getDifficultyColor(company.difficulty_level) }}>
                      {company.difficulty_display}
                    </div>
                    <div className="tag hiring-tag">
                      <Users size={12} />
                      {company.hiring_frequency_display}
                    </div>
                    {company.total_questions > 0 && (
                      <div className="tag questions-tag">
                        <Award size={12} />
                        {company.total_questions} Questions
                      </div>
                    )}
                  </div>
                </div>

                <div className="company-card-footer">
                  <button className="view-details-btn">
                    View Details
                    <ExternalLink size={16} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Companies;
