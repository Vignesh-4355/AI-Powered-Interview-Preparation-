import { useState } from 'react';
import { Upload, FileText, CheckCircle, XCircle, AlertCircle, TrendingUp, Target, Award, BarChart3 } from 'lucide-react';
import { resumeService, type ResumeAnalysis } from '../services/resumeService';
import './ResumeAnalyzer.css';

const ResumeAnalyzer = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null);
  const [error, setError] = useState('');
  const [dragOver, setDragOver] = useState(false);

  const handleFileSelect = (selectedFile: File) => {
    if (selectedFile.type !== 'application/pdf') {
      setError('Please select a PDF file');
      return;
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    setFile(selectedFile);
    setError('');
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      handleFileSelect(droppedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError('');

    try {
      const data = await resumeService.analyzeResume(file);
      setAnalysis(data.analysis);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to analyze resume');
    } finally {
      setUploading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return '#4caf50';
    if (score >= 60) return '#ff9800';
    return '#f44336';
  };

  return (
    <div className="resume-analyzer">
      <div className="page-header">
        <h1>AI Resume Analyzer</h1>
        <p>Get instant feedback on your resume with AI-powered analysis</p>
      </div>

      {/* Upload Section */}
      <div className="upload-section">
        <div
          className={`drop-zone ${dragOver ? 'drag-over' : ''}`}
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
        >
          <Upload size={48} className="upload-icon" />
          <h3>Drag & drop your resume here</h3>
          <p>or</p>
          <label className="file-input-label">
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => {
                if (e.target.files?.[0]) {
                  handleFileSelect(e.target.files[0]);
                }
              }}
              className="file-input"
            />
            Browse Files
          </label>
          <p className="file-types">PDF files only (max 10MB)</p>
        </div>

        {file && (
          <div className="file-info">
            <FileText size={20} />
            <span>{file.name}</span>
            <span className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</span>
            <button onClick={() => setFile(null)} className="remove-file">
              <XCircle size={18} />
            </button>
          </div>
        )}

        {error && (
          <div className="error-message">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="analyze-btn"
        >
          {uploading ? 'Analyzing...' : 'Analyze Resume'}
        </button>
      </div>

      {/* Analysis Results */}
      {analysis && (
        <div className="analysis-results">
          {/* Score Cards */}
          <div className="score-cards">
            <div className="score-card">
              <div className="score-icon" style={{ color: getScoreColor(analysis.skill_score) }}>
                <Award size={32} />
              </div>
              <div className="score-content">
                <h3>Skill Score</h3>
                <div className="score-value" style={{ color: getScoreColor(analysis.skill_score) }}>
                  {analysis.skill_score}%
                </div>
              </div>
            </div>

            <div className="score-card">
              <div className="score-icon" style={{ color: getScoreColor(analysis.formatting_score) }}>
                <FileText size={32} />
              </div>
              <div className="score-content">
                <h3>Formatting</h3>
                <div className="score-value" style={{ color: getScoreColor(analysis.formatting_score) }}>
                  {analysis.formatting_score}%
                </div>
              </div>
            </div>

            <div className="score-card">
              <div className="score-icon" style={{ color: getScoreColor(analysis.ats_score) }}>
                <BarChart3 size={32} />
              </div>
              <div className="score-content">
                <h3>ATS Score</h3>
                <div className="score-value" style={{ color: getScoreColor(analysis.ats_score) }}>
                  {analysis.ats_score}%
                </div>
              </div>
            </div>
          </div>

          {/* Detected Skills */}
          <div className="analysis-section">
            <h2 className="section-title">
              <CheckCircle size={24} className="icon-success" />
              Detected Skills ({analysis.detected_skills.length})
            </h2>
            <div className="skills-grid">
              {analysis.detected_skills.slice(0, 12).map((skillItem, idx) => (
                <div key={idx} className="skill-tag detected">
                  {skillItem.skill}
                  <span className="skill-category">{skillItem.category}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Missing Skills */}
          {analysis.missing_skills.length > 0 && (
            <div className="analysis-section">
              <h2 className="section-title">
                <Target size={24} className="icon-warning" />
                Missing Skills ({analysis.missing_skills.length})
              </h2>
              <div className="skills-grid">
                {analysis.missing_skills.slice(0, 8).map((skillItem, idx) => (
                  <div key={idx} className="skill-tag missing">
                    {skillItem.skill}
                    <span className="skill-priority">{skillItem.priority}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Keywords */}
          {analysis.keywords_found.length > 0 && (
            <div className="analysis-section">
              <h2 className="section-title">
                <TrendingUp size={24} />
                Top Keywords
              </h2>
              <div className="keywords-list">
                {analysis.keywords_found.map((keyword, idx) => (
                  <div key={idx} className="keyword-item">
                    <span className="keyword-name">{keyword.keyword}</span>
                    <div className="keyword-bar">
                      <div 
                        className="keyword-fill" 
                        style={{ width: `${Math.min(keyword.density * 10, 100)}%` }}
                      />
                    </div>
                    <span className="keyword-density">{keyword.density}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Strengths & Weaknesses */}
          <div className="feedback-grid">
            {analysis.strengths.length > 0 && (
              <div className="feedback-section strengths">
                <h3>
                  <CheckCircle size={20} className="icon-success" />
                  Strengths
                </h3>
                <ul>
                  {analysis.strengths.map((strength, idx) => (
                    <li key={idx}>{strength}</li>
                  ))}
                </ul>
              </div>
            )}

            {analysis.weaknesses.length > 0 && (
              <div className="feedback-section weaknesses">
                <h3>
                  <AlertCircle size={20} className="icon-error" />
                  Areas for Improvement
                </h3>
                <ul>
                  {analysis.weaknesses.map((weakness, idx) => (
                    <li key={idx}>{weakness}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Suggestions */}
          {analysis.suggestions.length > 0 && (
            <div className="analysis-section">
              <h2 className="section-title">
                <Target size={24} />
                Suggestions
              </h2>
              <ul className="suggestions-list">
                {analysis.suggestions.map((suggestion, idx) => (
                  <li key={idx}>{suggestion}</li>
                ))}
              </ul>
            </div>
          )}

          {/* ATS Issues */}
          {analysis.ats_issues.length > 0 && (
            <div className="analysis-section">
              <h2 className="section-title">
                <AlertCircle size={24} className="icon-warning" />
                ATS Compatibility Issues
              </h2>
              <ul className="ats-issues-list">
                {analysis.ats_issues.map((issue, idx) => (
                  <li key={idx}>
                    <XCircle size={16} className="icon-error" />
                    {issue}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ResumeAnalyzer;
