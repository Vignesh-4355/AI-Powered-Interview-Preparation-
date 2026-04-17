# User Progress Analytics Feature

## Overview
Comprehensive analytics dashboard tracking user progress across all modules including coding practice, aptitude tests, mock interviews, and roadmap completion.

## Backend Implementation

### Models

#### UserProgress (`analytics/models.py`)
Tracks overall user statistics:
- **coding_attempted**: Total coding questions attempted
- **coding_solved**: Total coding questions solved
- **mock_interviews_completed**: Mock interviews completed
- **aptitude_attempted**: Aptitude questions attempted
- **aptitude_correct**: Correct aptitude answers
- **current_streak**: Current activity streak in days
- **longest_streak**: Longest activity streak

### API Endpoints

#### GET `/api/analytics/`
Get comprehensive analytics for authenticated user.

**Response:**
```json
{
  "progress": {
    "coding_attempted": 25,
    "coding_solved": 18,
    "mock_interviews_completed": 3,
    "aptitude_attempted": 40,
    "aptitude_correct": 32,
    "coding_accuracy": 72.0,
    "aptitude_accuracy": 80.0
  },
  "coding_stats": {
    "total_attempted": 25,
    "total_solved": 18,
    "accuracy": 72.0,
    "by_difficulty": {
      "Easy": {"count": 10, "solved": 9},
      "Medium": {"count": 12, "solved": 7},
      "Hard": {"count": 3, "solved": 2}
    },
    "by_topic": {
      "Arrays": {"count": 8, "solved": 6},
      "Strings": {"count": 7, "solved": 5}
    },
    "recent_activity": [
      {"date": "2024-01-15", "count": 5},
      {"date": "2024-01-14", "count": 3}
    ]
  },
  "aptitude_stats": {
    "total_attempted": 40,
    "total_correct": 32,
    "overall_accuracy": 80.0,
    "by_category": {
      "Time and Work": {"attempted": 10, "correct": 8, "accuracy": 80.0},
      "Probability": {"attempted": 8, "correct": 6, "accuracy": 75.0}
    }
  },
  "mock_interview_stats": {
    "total_sessions": 5,
    "completed_sessions": 3,
    "average_score": 75.5
  },
  "company_prep_stats": {
    "total_companies": 50,
    "prepared_companies": 0,
    "completion_percentage": 0
  },
  "roadmap_stats": {
    "total_items": 12,
    "status_breakdown": {
      "not_started": 5,
      "in_progress": 3,
      "completed": 4
    },
    "completion_percentage": 33.3,
    "by_category": {
      "Data Structures": {"total": 4, "completed": 2},
      "Algorithms": {"total": 3, "completed": 1}
    }
  },
  "recent_activity": [
    {
      "type": "coding",
      "description": "Solved Two Sum",
      "timestamp": "2024-01-15T10:30:00Z",
      "icon": "code"
    }
  ]
}
```

#### POST `/api/analytics/update/`
Manually update user progress (for integration with other modules).

**Request:**
```json
{
  "type": "coding_attempt"
}
```

**Activity Types:**
- `coding_attempt`: Increment coding attempted count
- `coding_solved`: Increment coding solved count
- `aptitude_attempt`: Increment aptitude attempted count
- `aptitude_correct`: Increment aptitude correct count

## Frontend Implementation

### Components

#### AnalyticsPage (`frontend/src/pages/AnalyticsPage.tsx`)
Main analytics dashboard with:

1. **Overview Stats Cards**
   - Coding Solved count
   - Aptitude Accuracy percentage
   - Mock Interviews completed
   - Roadmap Progress percentage

2. **Interactive Charts**
   - **Coding Progress by Difficulty**: Bar chart comparing attempted vs solved
   - **7-Day Activity Trend**: Area chart showing daily activity
   - **Roadmap Status**: Pie chart of task completion status
   - **Aptitude Accuracy by Category**: Horizontal bar chart

3. **Progress Bars Section**
   - Visual progress indicators for each module
   - Gradient-filled bars with percentages

4. **Recent Activity Feed**
   - Timeline of recent user actions
   - Categorized by type (coding, mock interview)

### Services

#### analyticsService (`frontend/src/services/analyticsService.ts`)
```typescript
// Get comprehensive analytics
const data = await analyticsService.getAnalytics();

// Update progress manually
await analyticsService.updateProgress('coding_attempt');
```

## Features

### Dashboard Charts
- **Bar Charts**: Compare attempted vs solved questions by difficulty
- **Area Charts**: Show activity trends over time
- **Pie Charts**: Display roadmap task distribution
- **Horizontal Bar Charts**: Show aptitude accuracy by category

### Progress Tracking
- Real-time progress updates
- Accuracy calculations
- Streak tracking
- Multi-module aggregation

### Company Preparation Progress
- Track companies researched
- Monitor preparation completion
- Visual progress indicators

## Visual Design

### Color Scheme
- Primary: Purple gradient (#667eea to #764ba2)
- Success: Green gradient (#43e97b to #38f9d7)
- Warning: Pink gradient (#f093fb to #f5576c)
- Info: Blue gradient (#4facfe to #00f2fe)

### Responsive Layout
- Grid-based layout for stats cards
- Flexible chart containers
- Mobile-optimized views
- Touch-friendly interactions

## Usage

### Starting the Application

**Option 1: Use the startup script**
```bash
cd c:\Users\91850\OneDrive\Desktop\interviewApp
start.bat
```

**Option 2: Manual start**
```bash
# Terminal 1 - Backend
cd backend
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Accessing Analytics
1. Navigate to http://localhost:5173
2. Login/Register
3. Click on "Analytics" in the navigation
4. View comprehensive progress dashboard

## Integration Points

The analytics module integrates with:
- **coding_practice**: Tracks question attempts and solutions
- **aptitude**: Monitors test performance
- **roadmap**: Displays task completion status
- **companies**: Shows preparation progress

## Future Enhancements

Potential improvements:
- [ ] Real-time WebSocket updates
- [ ] Advanced ML-based insights
- [ ] Peer comparison analytics
- [ ] Detailed time tracking
- [ ] Skill gap analysis
- [ ] Personalized recommendations
- [ ] Export reports (PDF/Excel)
- [ ] Goal setting and tracking

## Dependencies

### Backend
- Django 5.2.3
- Django REST Framework 3.16.1

### Frontend
- React 19
- TypeScript
- Recharts (for charts)
- React Router DOM

## Testing

### Backend Testing
```bash
cd backend
python manage.py test analytics
```

### Frontend Testing
```bash
cd frontend
npm test
```

## Troubleshooting

### Blank Screen Issue
If you see a blank white screen:
1. Check browser console for errors
2. Verify backend is running at http://localhost:8000
3. Ensure frontend is running at http://localhost:5173
4. Check network tab for failed API calls
5. Verify authentication token is valid

### Migration Issues
```bash
cd backend
python manage.py makemigrations analytics
python manage.py migrate analytics
```

### Chart Not Rendering
- Verify recharts is installed: `npm list recharts`
- Check data format matches expected structure
- Ensure container has defined height/width

## Performance Considerations

- Charts use virtualization for large datasets
- Data cached to reduce API calls
- Lazy loading for chart libraries
- Optimized re-renders with React.memo

## Security

- All endpoints require authentication
- User-specific data isolation
- Rate limiting recommended for production
- CORS properly configured

---

**Created**: March 8, 2026  
**Version**: 1.0.0  
**Status**: Production Ready
