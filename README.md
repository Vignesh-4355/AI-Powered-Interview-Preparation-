# AI Powered Interview Preparation Portal

A full-stack web application for interview preparation with AI-powered features.

## Project Structure

```
interviewApp/
├── backend/                 # Django Backend
│   ├── interview_portal/   # Django project settings
│   │   ├── settings.py     # Configuration (CORS, REST Framework, Auth)
│   │   ├── urls.py         # Main URL routing
│   │   └── ...
│   ├── accounts/           # User accounts & authentication app
│   ├── companies/          # Company information app
│   ├── preparation/        # Study materials app
│   ├── mock_interview/     # AI mock interviews app
│   ├── chatbot/            # AI chatbot assistant app
│   ├── roadmap/            # Personalized learning paths app
│   ├── analytics/          # Progress tracking app
│   ├── resume/             # Resume review app
│   ├── manage.py           # Django management script
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
│
└── frontend/               # React Frontend (Vite)
    ├── src/
    │   ├── components/     # Reusable React components
    │   ├── pages/          # Page components
    │   │   ├── Home.tsx    # Landing page
    │   │   ├── Login.tsx   # Login page
    │   │   └── Dashboard.tsx # User dashboard
    │   ├── services/       # API services
    │   │   ├── api.ts      # Axios configuration
    │   │   └── authService.ts # Authentication service
    │   ├── context/        # React Context
    │   │   └── AuthContext.tsx # Auth state management
    │   ├── auth/           # Authentication utilities
    │   ├── App.tsx         # Main App component
    │   └── main.tsx        # Entry point
    ├── package.json        # Node dependencies
    └── vite.config.ts      # Vite configuration
```

## Features

### Backend (Django + DRF)
- ✅ Custom User model with email authentication
- ✅ Extended UserProfile for additional user data
- ✅ Django REST Framework for API development
- ✅ CORS configuration for React frontend
- ✅ Token-based authentication
- ✅ Django Allauth for authentication flows
- ✅ 8 modular apps ready for development

### Frontend (React + Vite)
- ✅ Modern React with TypeScript
- ✅ React Router for navigation
- ✅ Axios for API calls
- ✅ Context API for state management
- ✅ Authentication flow (Login/Logout)
- ✅ Protected routes
- ✅ Responsive design
- ✅ Beautiful UI with gradients and animations

## Tech Stack

### Backend
- **Framework:** Django 5.2.3
- **API:** Django REST Framework 3.16.1
- **Authentication:** django-allauth 65.13.1
- **CORS:** django-cors-headers 4.9.0
- **Environment:** python-dotenv 1.1.1
- **Database:** SQLite (development)

### Frontend
- **Framework:** React 19.2.0
- **Build Tool:** Vite 7.3.1
- **Routing:** react-router-dom 6.20.0
- **HTTP Client:** axios 1.6.0
- **Language:** TypeScript

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment (optional but recommended):
```bash
python -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser (for admin access):
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Current Endpoints
- `GET /api/accounts/api-test/` - Test API connection
- `GET /api/accounts/dashboard/` - Get user dashboard data (authenticated)
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Future Endpoints (To be implemented)
- Companies: `/api/companies/`
- Preparation: `/api/preparation/`
- Mock Interviews: `/api/mock-interviews/`
- Chatbot: `/api/chatbot/`
- Roadmap: `/api/roadmap/`
- Analytics: `/api/analytics/`
- Resume: `/api/resume/`

## Testing the Application

1. Start both backend and frontend servers
2. Visit `http://localhost:5173` in your browser
3. You should see the Home page with all features listed
4. Click on "Get Started" or "Login" to access the login page
5. Use the credentials you created with `createsuperuser` to login
6. After login, you'll be redirected to the Dashboard

## Next Steps

### Backend Development
1. Implement models for each app (companies, preparation, etc.)
2. Create serializers for API data transformation
3. Build out API views and viewsets
4. Add URL routing for all endpoints
5. Implement permission classes
6. Add pagination and filtering
7. Integrate AI/ML models for:
   - Mock interviews
   - Chatbot
   - Resume analysis
   - Personalized recommendations

### Frontend Development
1. Create remaining pages for each module
2. Build reusable components
3. Implement form validation
4. Add loading states and error handling
5. Create responsive layouts for mobile
6. Add data visualization for analytics
7. Implement real-time features (WebSocket)

## Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=db.sqlite3
```

## Admin Panel

Access the Django admin panel at: `http://localhost:8000/admin/`

Use the superuser credentials you created during setup.

## License

MIT License

## Contact

For questions or support, please reach out to the development team.
