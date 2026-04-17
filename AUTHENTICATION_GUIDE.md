# 🔐 Authentication System - Complete Guide

## Overview

A complete JWT-based authentication system with email signup, login, Google OAuth, and protected routes.

---

## ✅ Features Implemented

### Backend (Django + DRF)

**Authentication Methods:**
- ✅ Email-based registration
- ✅ Email/password login with JWT tokens
- ✅ Google OAuth integration
- ✅ UserProfile model extension
- ✅ Token refresh mechanism
- ✅ Token blacklisting on logout

**API Endpoints:**
```
POST   /api/accounts/register/     - User registration
POST   /api/accounts/login/        - User login
POST   /api/accounts/logout/       - User logout
GET    /api/accounts/profile/      - Get user profile
GET    /api/accounts/dashboard/    - Get dashboard data
GET    /api/accounts/api-test/     - API health check
POST   /api/token/                 - Get JWT token pair
POST   /api/token/refresh/         - Refresh access token
```

**Security Features:**
- JWT tokens with expiration (60 min access, 7 days refresh)
- Password validation (min 8 characters)
- Email uniqueness validation
- Token blacklisting
- CORS configuration
- CSRF protection

### Frontend (React + Vite)

**Pages:**
- ✅ **Login Page** - Modern UI with Google OAuth button
- ✅ **Register Page** - Complete registration form with validation
- ✅ **Dashboard** - Protected user dashboard
- ✅ **Home Page** - Public landing page

**Components:**
- ✅ **ProtectedRoute** - Route guard for authenticated pages
- ✅ **AuthContext** - Global authentication state
- ✅ **AuthService** - API integration layer

**Features:**
- JWT token storage in localStorage
- Automatic token handling
- Protected routes
- Loading states
- Error handling
- Form validation
- Google OAuth redirect

---

## 🚀 Setup Instructions

### Backend Setup

1. **Install Dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Run Migrations**:
```bash
python manage.py migrate
```

3. **Create Superuser** (optional):
```bash
python manage.py createsuperuser
```

4. **Configure Google OAuth** (Optional):
   - Get credentials from [Google Cloud Console](https://console.cloud.google.com/)
   - Update `.env` file:
```env
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_SECRET=your-secret
```
   - Or update `settings.py` directly in `SOCIALACCOUNT_PROVIDERS`

5. **Start Server**:
```bash
python manage.py runserver
```

### Frontend Setup

1. **Install Dependencies**:
```bash
cd frontend
npm install
```

2. **Start Development Server**:
```bash
npm run dev
```

3. **Access Application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api/

---

## 📝 API Documentation

### 1. Register User

**Endpoint**: `POST /api/accounts/register/`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response** (201 Created):
```json
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Response** (400 Bad Request):
```json
{
  "email": ["Email is already registered"],
  "password": ["Password must be at least 8 characters"]
}
```

---

### 2. Login

**Endpoint**: `POST /api/accounts/login/`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Response** (401 Unauthorized):
```json
{
  "error": "Invalid email or password"
}
```

---

### 3. Logout

**Endpoint**: `POST /api/accounts/logout/`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Request Body**:
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):
```json
{
  "message": "Logout successful"
}
```

---

### 4. Get Profile

**Endpoint**: `GET /api/accounts/profile/`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": null
  },
  "profile": {
    "user": {...},
    "avatar": null,
    "bio": "",
    "target_job_role": "Software Engineer",
    "experience_level": "mid",
    "preferred_locations": "San Francisco, CA",
    "created_at": "2026-03-06T...",
    "updated_at": "2026-03-06T..."
  }
}
```

---

## 🔧 Frontend Usage

### Using AuthService

```typescript
import { authService } from './services/authService';

// Register
try {
  const response = await authService.register({
    email: 'user@example.com',
    password: 'password123',
    password_confirm: 'password123',
    first_name: 'John',
    last_name: 'Doe'
  });
  console.log('Registered:', response.user);
} catch (error) {
  console.error('Registration failed:', error);
}

// Login
try {
  const response = await authService.login({
    email: 'user@example.com',
    password: 'password123'
  });
  console.log('Logged in:', response.user);
} catch (error) {
  console.error('Login failed:', error);
}

// Get Profile
try {
  const profile = await authService.getProfile();
  console.log('User profile:', profile);
} catch (error) {
  console.error('Failed to fetch profile:', error);
}

// Logout
await authService.logout();
```

### Using AuthContext

```typescript
import { useAuth } from './context/AuthContext';

function MyComponent() {
  const { user, login, logout, isAuthenticated, loading } = useAuth();

  const handleLogin = async () => {
    try {
      await login({ email: 'user@example.com', password: 'password123' });
      console.log('Logged in as:', user);
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  const handleLogout = async () => {
    await logout();
    console.log('Logged out');
  };

  if (loading) return <div>Loading...</div>;
  
  return (
    <div>
      {isAuthenticated ? (
        <div>Welcome, {user?.email}!</div>
      ) : (
        <button onClick={handleLogin}>Login</button>
      )}
    </div>
  );
}
```

### Protected Routes

```typescript
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/public" element={<PublicPage />} />
        <Route
          path="/protected"
          element={
            <ProtectedRoute>
              <ProtectedPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}
```

---

## 🎨 UI Components

### Login Page Features

- Modern gradient background
- Email/password form
- Google OAuth button
- Form validation
- Error messages
- Loading states
- Responsive design
- Back navigation

### Register Page Features

- Two-column name fields
- Email validation
- Password strength validation
- Password confirmation
- Form validation
- Error messages
- Loading states
- Responsive design

### ProtectedRoute Component

- Checks authentication status
- Shows loading spinner while verifying
- Redirects to login if not authenticated
- Preserves intended destination

---

## 🔐 Security Best Practices

### Token Management

1. **Storage**: Tokens stored in localStorage (consider httpOnly cookies for production)
2. **Expiration**: 
   - Access token: 60 minutes
   - Refresh token: 7 days
3. **Blacklisting**: Refresh tokens blacklisted on logout
4. **Rotation**: New refresh token issued on each refresh

### Password Security

- Minimum 8 characters
- Not stored in plain text
- Hashed using Django's PBKDF2 algorithm

### CORS Configuration

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
CORS_ALLOW_CREDENTIALS = True
```

---

## 🐛 Troubleshooting

### Common Issues

**1. CORS Errors**

**Error**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:5173' has been blocked by CORS policy`

**Solution**: 
- Ensure `django-cors-headers` is installed
- Check `CORS_ALLOWED_ORIGINS` in settings.py
- Verify `CorsMiddleware` is in MIDDLEWARE

**2. Token Expired**

**Error**: `Token has expired`

**Solution**:
- Use refresh token to get new access token
- Implement automatic token refresh in axios interceptor

**3. Invalid Credentials**

**Error**: `Invalid email or password`

**Solution**:
- Check email spelling
- Verify password matches
- Ensure user is registered

**4. Google OAuth Not Working**

**Error**: Redirect URI mismatch

**Solution**:
- Add `http://localhost:8000` to authorized redirect URIs in Google Cloud Console
- Check Google OAuth credentials in settings.py

---

## 📦 File Structure

```
backend/
├── accounts/
│   ├── models.py           # User, UserProfile
│   ├── serializers.py      # RegisterSerializer, CustomTokenObtainPairSerializer
│   ├── views.py            # register, login, logout, profile views
│   ├── urls.py             # API endpoints
│   └── admin.py            # Admin configuration
└── interview_portal/
    └── settings.py         # JWT, REST Framework, Allauth config

frontend/
├── src/
│   ├── components/
│   │   └── ProtectedRoute.tsx    # Route guard
│   ├── pages/
│   │   ├── Login.tsx             # Login page with Google OAuth
│   │   ├── Register.tsx          # Registration page
│   │   └── Dashboard.tsx         # Protected dashboard
│   ├── services/
│   │   └── authService.ts        # API service layer
│   └── context/
│       └── AuthContext.tsx       # Global auth state
```

---

## 🎯 Next Steps

### Enhancements

1. **Password Reset**: Implement forgot password flow
2. **Email Verification**: Require email confirmation
3. **Two-Factor Authentication**: Add 2FA support
4. **Social Login**: Add more providers (GitHub, LinkedIn)
5. **Account Settings**: Profile editing page
6. **Session Management**: View active sessions

### Production Considerations

1. **HTTPS**: Always use HTTPS in production
2. **Secure Cookies**: Store tokens in httpOnly cookies
3. **Rate Limiting**: Prevent brute force attacks
4. **Monitoring**: Log authentication attempts
5. **Token Storage**: Use secure storage mechanisms
6. **CSRF Protection**: Enable CSRF tokens

---

## 📚 Additional Resources

- [Django REST Framework SimpleJWT Docs](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Django Allauth Documentation](https://django-allauth.readthedocs.io/)
- [React Router v6](https://reactrouter.com/)
- [JWT.io](https://jwt.io/) - Decode and verify JWT tokens

---

**Last Updated**: March 6, 2026  
**Version**: 2.0.0  
**Status**: Production Ready
