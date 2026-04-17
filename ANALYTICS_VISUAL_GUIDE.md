# Analytics Dashboard - Visual Guide

## 🎯 What You'll See

### Page Layout
```
┌─────────────────────────────────────────────────────┐
│  Your Progress Analytics                            │
│  Track your interview preparation journey          │
└─────────────────────────────────────────────────────┘

┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ 📚       │ │ 🎯       │ │ 🎬       │ │ 📊       │
│ Coding   │ │ Aptitude │ │ Mock     │ │ Roadmap  │
│ Solved   │ │ Accuracy │ │ Interviews│ │ Progress │
│          │ │          │ │          │ │          │
│    18    │ │   80.0%  │ │    3     │ │   33%    │
│ out of 25│ │ 32 correct│ │ avg: 75.5│ │ 4 tasks  │
└──────────┘ └──────────┘ └──────────┘ └──────────┘

┌─────────────────────────────────────────────────────┐
│ Coding Progress by Difficulty                       │
│                                                     │
│  [Bar Chart: Easy/Medium/Hard]                     │
│  Purple bars = Attempted                           │
│  Green bars = Solved                               │
└─────────────────────────────────────────────────────┘

┌──────────────────┐ ┌──────────────────┐
│ 7-Day Activity   │ │ Roadmap Status   │
│                  │ │                  │
│ [Area Chart]     │ │  [Pie Chart]     │
│ Shows daily      │ │  Completed/In    │
│ coding activity  │ │  Progress/Not    │
│                  │ │  Started         │
└──────────────────┘ └──────────────────┘

┌─────────────────────────────────────────────────────┐
│ Aptitude Accuracy by Category                       │
│                                                     │
│  [Horizontal Bar Chart]                            │
│  Time & Work, Distance, Probability, etc.          │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Detailed Progress                                   │
│                                                     │
│ Coding Mastery      [████████░░] 72%               │
│ Aptitude Skills     [█████████░] 80%               │
│ Mock Interview      [███████░░░] 75%               │
│ Roadmap Completion  [████░░░░░░] 33%               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ Recent Activity                                     │
│                                                     │
│ 💻 Solved Two Sum                    Jan 15, 2024  │
│ 💻 Attempted Reverse Linked List     Jan 14, 2024  │
│ 💻 Solved Valid Parentheses          Jan 14, 2024  │
└─────────────────────────────────────────────────────┘
```

## 🎨 Color Scheme

### Stats Cards
- **Purple** (Primary) - Coding statistics
- **Green** (Success) - Aptitude accuracy  
- **Pink** (Warning) - Mock interviews
- **Blue** (Info) - Roadmap progress

### Progress Bars
- **Purple Gradient** - Coding mastery
- **Green Gradient** - Aptitude skills
- **Pink Gradient** - Mock interview performance
- **Blue Gradient** - Roadmap completion

### Charts
- **Purple** (#667eea) - Attempted/Active data
- **Green** (#43e97b) - Solved/Completed data
- **Pink** (#f093fb) - Interview data
- **Blue** (#4facfe) - Roadmap data

## 📱 Responsive Behavior

### Desktop (> 768px)
- 4-column grid for stats cards
- 2-column grid for charts
- Full-width progress section
- Side-by-side activity items

### Mobile (≤ 768px)
- Single column layout
- Stacked stats cards
- Full-width charts
- Vertical activity list
- Smaller fonts and icons

## 🖱️ Interactive Elements

### Hover Effects
- **Stats Cards**: Lift up with shadow
- **Chart Bars**: Show tooltips with details
- **Activity Items**: Background highlight

### Click Actions
- **Chart Legends**: Toggle data series
- **Progress Bars**: None (visual only)
- **Activity Items**: Future deep-link capability

## 🔄 Data Flow

```
User Login → Auth Token
    ↓
Navigate to Analytics
    ↓
Frontend calls GET /api/analytics/
    ↓
Backend aggregates data from:
  - coding_practice module
  - aptitude module
  - roadmap module
  - companies module
    ↓
Returns JSON response
    ↓
Frontend parses data
    ↓
Charts render with Recharts
    ↓
User sees comprehensive dashboard
```

## 📊 Sample Data Display

### Before Any Activity
```
Coding Solved: 0
Aptitude Accuracy: 0%
Mock Interviews: 0
Roadmap Progress: 0%
Message: "No analytics data available"
```

### After Some Activity
```
Coding Solved: 18/25 (72%)
Aptitude Accuracy: 80% (32/40)
Mock Interviews: 3 completed
Roadmap Progress: 33% (4/12 tasks)

Recent Activity:
- Solved "Two Sum" (Easy) - Arrays
- Attempted "Reverse Linked List" (Medium)
- Completed Mock Interview #3 (Score: 78)
```

## 🎯 Key Metrics Explained

### Coding Mastery
- **Formula**: (Solved / Attempted) × 100
- **Display**: Percentage + progress bar
- **Color**: Purple gradient
- **Data Source**: coding_practice.UserProgress

### Aptitude Accuracy
- **Formula**: (Correct / Attempted) × 100
- **Display**: Percentage + category breakdown
- **Color**: Green gradient
- **Data Source**: aptitude.UserAttempt

### Mock Interview Performance
- **Formula**: Average of all completed scores
- **Display**: Average score + count
- **Color**: Pink gradient
- **Data Source**: mock_interview.MockInterviewSession

### Roadmap Completion
- **Formula**: (Completed / Total) × 100
- **Display**: Percentage + task count
- **Color**: Blue gradient
- **Data Source**: roadmap.RoadmapItem

## 🧩 Component Structure

```
AnalyticsPage
├── page-header
│   ├── Title
│   └── Subtitle
├── stats-overview
│   ├── stat-card (primary) - Coding
│   ├── stat-card (success) - Aptitude
│   ├── stat-card (warning) - Mock Interviews
│   └── stat-card (info) - Roadmap
├── charts-grid
│   ├── chart-card (full-width) - Coding Difficulty
│   ├── chart-card - Activity Trend
│   ├── chart-card - Roadmap Status
│   └── chart-card (full-width) - Aptitude Categories
├── progress-section
│   ├── progress-item - Coding Mastery
│   ├── progress-item - Aptitude Skills
│   ├── progress-item - Mock Performance
│   └── progress-item - Roadmap Completion
└── recent-activity-section
    └── activity-list
        └── activity-item (multiple)
```

## 🎭 Animations

### Loading State
- Centered spinner
- "Loading analytics..." text
- No background content

### Data Load
- Fade-in animation for cards
- Stagger animation for stats (100ms delay each)
- Chart rendering animation (smooth draw)

### Progress Bars
- Width transition (0.5s ease)
- Smooth fill animation

### Hover States
- Card lift: `transform: translateY(-5px)`
- Shadow increase: `box-shadow: 0 8px 20px`
- Transition: 0.3s ease

## 📐 Dimensions

### Stats Cards
- Min width: 280px
- Padding: 1.5rem
- Gap: 1.5rem
- Border radius: 16px

### Charts
- Container height: 250-300px
- Full width on mobile
- Grid gap: 1.5rem

### Progress Bars
- Height: 12px
- Border radius: 6px
- Fill transition: 0.5s

### Typography
- Page title: 2.5rem
- Card headers: 0.9rem
- Stat values: 2rem
- Subtitles: 0.85rem

---

**Ready to Use!** 🚀

Access your analytics at: http://localhost:5173/analytics
