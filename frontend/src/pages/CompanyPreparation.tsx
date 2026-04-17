import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Building2, Search } from 'lucide-react';
import { companyService, type Company } from '../services/companyService';
import './CompanyPreparation.css';

const CompanyPreparation = () => {
  const navigate = useNavigate();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredCompanies, setFilteredCompanies] = useState<Company[]>([]);

  useEffect(() => {
    fetchCompanies();
  }, []);

  useEffect(() => {
    filterCompanies();
  }, [searchQuery, companies]);

  const fetchCompanies = async () => {
    try {
      setLoading(true);
      const data = await companyService.getAllCompanies();
      setCompanies(data);
      setFilteredCompanies(data);
    } catch (err: any) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filterCompanies = () => {
    if (!searchQuery.trim()) {
      setFilteredCompanies(companies);
      return;
    }

    const filtered = companies.filter(company =>
      company.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      company.description?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      company.industry?.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredCompanies(filtered);
  };

  const handleCompanyClick = (companyId: number) => {
    navigate(`/companies/${companyId}`);
  };

  if (loading) {
    return (
      <div className="company-prep-container">
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading companies...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="company-prep-container">
      <div className="prep-header">
        <Link to="/dashboard" className="back-button">
          <ArrowLeft size={20} />
          Back to Dashboard
        </Link>
        
        <div className="header-content">
          <Building2 size={48} className="header-icon" />
          <h1>Company Specific Preparation</h1>
          <p className="subtitle">
            Choose a company to explore its interview pattern, questions, and preparation resources
          </p>
        </div>
      </div>

      <div className="search-section">
        <div className="search-box">
          <Search size={20} className="search-icon" />
          <input
            type="text"
            placeholder="Search companies by name, description, or industry..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
        </div>
      </div>

      <div className="companies-grid">
        {filteredCompanies.length === 0 ? (
          <div className="no-results">
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
                {company.logo ? (
                  <img src={company.logo} alt={company.name} className="company-logo" />
                ) : (
                  <div className="company-logo-placeholder">
                    <Building2 size={32} />
                  </div>
                )}
                <h3 className="company-name">{company.name}</h3>
              </div>
              
              <div className="company-card-body">
                <p className="company-description">
                  {company.description || 'No description available'}
                </p>
                
                {company.industry && (
                  <div className="company-industry">
                    <strong>Industry:</strong> {company.industry}
                  </div>
                )}
                
                {company.total_questions !== undefined && (
                  <div className="company-stats">
                    <span className="stat-badge">
                      📝 {company.total_questions} Questions
                    </span>
                  </div>
                )}
              </div>
              
              <div className="company-card-footer">
                <span className="view-details-btn">View Details →</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default CompanyPreparation;
