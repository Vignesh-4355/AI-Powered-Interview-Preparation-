# Quick Start Guide - AI Powered Interview Preparation Portal

## 🚀 Get Started in 5 Minutes

### Prerequisites Check
- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ Git installed (optional)

### Option 1: Automated Setup (Recommended for Windows)

1. **Run the setup script**:
```bash
# Double-click setup.bat or run from command line
.\setup.bat
```

This will:
- Create virtual environment
- Install all dependencies
- Run database migrations
- Create admin user
- Set up frontend

2. **Start the servers**:
```bash
# Double-click start-servers.bat or run from command line
.\start-servers.bat
```

### Option 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (optional)
python -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (for admin panel)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Backend running at: **http://localhost:8000**

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend running at: **http://localhost:5173**

## 📱 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | Use registered email/password |
| Admin Panel | http://localhost:8000/admin | Superuser credentials |
| API Test | http://localhost:8000/api/accounts/api-test/ | Public access |

## ✅ Verify Installation

### 1. Test Backend
Open browser and visit:
```
http://localhost:8000/api/accounts/api-test/
```

You should see:
```json
{
  "message": "AI Powered Interview Preparation Portal API is running!",
  "version": "1.0.0",
  "status": "healthy"
}
```

### 2. Test Frontend
Open browser and visit:
```
http://localhost:5173
```

You should see the Home page with:
- Hero section
- Feature cards
- Navigation buttons

### 3. Test Login
1. Click "Login" button on home page
2. Enter your superuser credentials
3. You should be redirected to Dashboard

## 🎯 First Steps

### Explore the Dashboard

After logging in, you'll see:
- **Welcome Section**: Personalized greeting
- **Profile Summary**: Your job preferences
- **Module Cards**: Quick access to all features
- **Quick Stats**: Your progress metrics

### Access Admin Panel

1. Visit: http://localhost:8000/admin/
2. Login with superuser credentials
3. Explore:
   - Users management
   - User profiles
   - System settings

## 🛠️ Development Commands

### Backend

```bash
# Run server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Open Django shell
python manage.py shell
```

### Frontend

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Install new package
npm install package-name
```

## 📁 Project Structure Quick Reference

```
interviewApp/
├── backend/              # Django backend
│   ├── accounts/        # User management
│   ├── companies/       # Company info
│   ├── preparation/     # Study materials
│   ├── mock_interview/  # Mock interviews
│   ├── chatbot/         # AI chatbot
│   ├── roadmap/         # Learning paths
│   ├── analytics/       # Progress tracking
│   └── resume/          # Resume review
│
└── frontend/            # React frontend
    ├── src/
    │   ├── pages/      # Page components
    │   ├── services/   # API calls
    │   └── context/    # Global state
    └── public/         # Static assets
```

## 🔧 Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError`
```bash
# Solution: Ensure virtual environment is activated
.\venv\Scripts\Activate
pip install -r requirements.txt
```

**Error**: `Port 8000 already in use`
```bash
# Solution: Use different port
python manage.py runserver 8001
```

### Frontend won't start

**Error**: `npm command not found`
```bash
# Solution: Install Node.js from nodejs.org
```

**Error**: `Cannot find module`
```bash
# Solution: Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors

**Error**: `CORS policy blocking request`
```bash
# Solution: Check backend settings.py
# Ensure CORS_ALLOWED_ORIGINS includes http://localhost:5173
```

### Database Issues

**Error**: `no such table`
```bash
# Solution: Run migrations
python manage.py migrate
```

## 📝 Next Steps

1. ✅ Complete setup
2. ✅ Test basic functionality
3. 📖 Read PROJECT_OVERVIEW.md for detailed architecture
4. 🧪 Check API_TESTING.md for testing guide
5. 💻 Start developing features

## 🆘 Getting Help

### Documentation
- **README.md**: General overview
- **PROJECT_OVERVIEW.md**: Detailed architecture
- **API_TESTING.md**: API testing guide

### Common Tasks

**Create a new user**:
```bash
# Via admin panel
Visit: http://localhost:8000/admin/
Click: Users → Add User
```

**Reset password**:
```bash
# Via Django shell
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(email='your@email.com')
>>> user.set_password('newpassword')
>>> user.save()
```

**Clear database and start fresh**:
```bash
# Delete database file and recreate
rm db.sqlite3
python manage.py migrate
```

## 🎉 Success Indicators

You know everything is working when:

✅ Backend starts without errors  
✅ Frontend starts without errors  
✅ API test endpoint returns healthy status  
✅ Can login with credentials  
✅ Dashboard loads successfully  
✅ No console errors in browser  

## 📞 Support

If you encounter issues:

1. Check error messages carefully
2. Review this guide
3. Check documentation files
4. Search for error online
5. Ask in community forums

---

**Ready to start building?** 

Visit http://localhost:5173 and begin your interview preparation journey! 🚀

**Last Updated**: March 6, 2026  
**Version**: 1.0.0
