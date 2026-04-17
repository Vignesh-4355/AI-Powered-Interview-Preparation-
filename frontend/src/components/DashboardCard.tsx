import type { LucideIcon } from 'lucide-react';
import { Link } from 'react-router-dom';
import './DashboardCard.css';

interface DashboardCardProps {
  title: string;
  icon: LucideIcon;
  description: string;
  buttonText: string;
  to: string;
  color?: string;
}

export const DashboardCard: React.FC<DashboardCardProps> = ({
  title,
  icon: Icon,
  description,
  buttonText,
  to,
  color = '#667eea'
}) => {
  return (
    <div className="dashboard-card">
      <div className="card-header">
        <div 
          className="icon-container" 
          style={{ 
            background: `linear-gradient(135deg, ${color}20, ${color}40)`,
            borderColor: color
          }}
        >
          <Icon size={32} color={color} />
        </div>
      </div>
      
      <div className="card-body">
        <h3 className="card-title">{title}</h3>
        <p className="card-description">{description}</p>
      </div>
      
      <div className="card-footer">
        <Link to={to} className="card-button" style={{ borderColor: color, color: color }}>
          {buttonText} →
        </Link>
      </div>
    </div>
  );
};
