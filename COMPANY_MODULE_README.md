# Company Specific Preparation Module

Complete implementation of the Company Specific Preparation module for the AI Powered Interview Preparation Portal.

## 📋 Features

### Backend (Django REST Framework)

#### Models
1. **Company**
   - name, description, logo (URL), website, industry
   - Timestamps (created_at, updated_at)

2. **CompanyInterviewPattern**
   - Foreign Key to Company
   - round_name (Aptitude, Technical, HR, Coding, Group Discussion, Managerial)
   - description, duration, order
   - Tracks interview process rounds

3. **CompanyQuestion**
   - Foreign Key to Company
   - question (text), question_type (HR/Technical/Coding/Aptitude/Behavioral)
   - answer, youtube_link, difficulty (Easy/Medium/Hard)
   - tags for categorization

#### API Endpoints

```
GET    /api/companies/                    - List all companies
GET    /api/companies/{id}/               - Get company details
GET    /api/companies/{id}/patterns/      - Get interview patterns
GET    /api/companies/{id}/questions/     - Get questions (with filters)
GET    /api/companies/{id}/details/       - Complete company details
GET    /api/questions/                    - All questions (filterable)
```

**Query Parameters:**
- `?search=query` - Search companies by name
- `?type=HR|Technical|Coding|Aptitude` - Filter questions by type
- `?difficulty=Easy|Medium|Hard` - Filter questions by difficulty

### Frontend (React + TypeScript)

#### Components

1. **CompanyPreparation Page** (`/companies-prep`)
   - Grid layout displaying all companies
   - Search functionality
   - Company cards with logo, description, industry, question count
   - Click to view detailed information

2. **CompanyDetail Page** (`/companies/:id`)
   - Three tabs: Overview, Interview Pattern, Questions
   - **Overview**: Company info, stats
   - **Interview Pattern**: Timeline of interview rounds
   - **Questions**: Filterable list with expandable answers
     - Filter by question type (All/HR/Technical/Coding)
     - Difficulty badges (color-coded)
     - YouTube links for video explanations
     - Tags for categorization

#### Services
- `companyService.ts` - API integration with TypeScript interfaces

## 🎨 UI Features

- Modern gradient design matching portal theme
- Responsive grid layouts
- Smooth animations and hover effects
- Color-coded difficulty levels
- Interactive tabs and filters
- Loading states and error handling
- Mobile-responsive design

## 📦 Sample Data

Pre-populated with 4 companies:
1. **TCS** - 3 interview rounds, 4 questions
2. **Infosys** - 4 interview rounds, 3 questions
3. **Amazon** - 4 interview rounds, 3 questions (includes behavioral/leadership principles)
4. **Wipro** - 3 interview rounds, 2 questions

## 🚀 Usage

### Backend Setup

1. Apply migrations:
```bash
cd backend
python manage.py makemigrations companies
python manage.py migrate
```

2. Populate sample data:
```bash
python manage.py populate_companies
```

3. Run server:
```bash
python manage.py runserver
```

### Frontend Setup

The frontend is already configured. Just ensure the dev server is running:
```bash
cd frontend
npm run dev
```

## 🧪 Testing the Module

1. Navigate to Dashboard
2. Click "Company Specific Preparation" card
3. Browse available companies
4. Use search to filter companies
5. Click on any company (e.g., Amazon)
6. Explore tabs:
   - **Overview**: Company details
   - **Interview Pattern**: Step-by-step process
   - **Questions**: Practice questions with filters

## 📁 Files Created

### Backend
```
backend/companies/
├── models.py                 # Company, CompanyInterviewPattern, CompanyQuestion
├── serializers.py            # CompanySerializer, patterns, questions serializers
├── views.py                  # CompanyViewSet, CompanyQuestionViewSet
├── urls.py                   # Router configuration
└── management/commands/
    └── populate_companies.py # Sample data population
```

### Frontend
```
frontend/src/
├── services/
│   └── companyService.ts     # API service with TypeScript interfaces
├── pages/
│   ├── CompanyPreparation.tsx     # Company list page
│   ├── CompanyPreparation.css     # Styling for list page
│   ├── CompanyDetail.tsx          # Company detail page
│   └── CompanyDetail.css          # Styling for detail page
└── App.tsx                   # Updated with new routes
```

## 🔐 Security Notes

- Currently allows unauthenticated access (AllowAny permissions)
- Can be restricted by changing to `IsAuthenticated` permission class
- JWT token support ready in API interceptor

## 🎯 Future Enhancements

- [ ] Admin panel customization for easy content management
- [ ] User progress tracking per company
- [ ] Bookmarking favorite questions
- [ ] Mock interview scheduling per company pattern
- [ ] Company reviews and ratings
- [ ] Salary insights
- [ ] More companies and questions
- [ ] Video solutions integration
- [ ] Difficulty-based learning paths

## 📊 API Response Examples

### GET /api/companies/
```json
[
  {
    "id": 1,
    "name": "TCS",
    "description": "Tata Consultancy Services...",
    "logo": "https://...",
    "industry": "IT Services & Consulting"
  }
]
```

### GET /api/companies/1/patterns/
```json
[
  {
    "id": 1,
    "round_name": "Aptitude",
    "round_name_display": "Aptitude Test",
    "description": "Online aptitude test...",
    "duration": "90 minutes",
    "order": 1
  }
]
```

### GET /api/companies/1/questions/
```json
[
  {
    "id": 1,
    "question": "Tell me about yourself...",
    "question_type": "HR",
    "question_type_display": "HR Question",
    "answer": "Start with your background...",
    "difficulty": "Easy",
    "difficulty_display": "Easy",
    "youtube_link": null,
    "tags": "introduction, motivation"
  }
]
```

---

**Module Status**: ✅ Complete and Ready for Production
