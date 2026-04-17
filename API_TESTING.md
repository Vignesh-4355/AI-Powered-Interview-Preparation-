# API Testing Guide

## Testing the Backend API

### 1. Test API Connection

**Endpoint**: `GET http://localhost:8000/api/accounts/api-test/`

**Expected Response**:
```json
{
  "message": "AI Powered Interview Preparation Portal API is running!",
  "version": "1.0.0",
  "status": "healthy"
}
```

**Using curl**:
```bash
curl http://localhost:8000/api/accounts/api-test/
```

**Using browser**:
Simply visit: http://localhost:8000/api/accounts/api-test/

### 2. Test Dashboard (Requires Authentication)

**Endpoint**: `GET http://localhost:8000/api/accounts/dashboard/`

**Headers**:
```
Authorization: Token YOUR_TOKEN_HERE
```

**Expected Response**:
```json
{
  "user": {
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "profile": {
    "target_job_role": "Software Engineer",
    "experience_level": "mid",
    "bio": "..."
  }
}
```

## Testing with Postman

### Setup

1. **Create a new Collection**: "Interview Portal API"

2. **Add Base URL Variable**:
   - Name: `baseUrl`
   - Value: `http://localhost:8000`

3. **Add Authorization**:
   - Type: Token Auth
   - Token: `{{your_token}}`

### Test Requests

#### 1. API Health Check
- **Method**: GET
- **URL**: `{{baseUrl}}/api/accounts/api-test/`
- **Auth**: None
- **Expected**: 200 OK with health status

#### 2. User Login
- **Method**: POST
- **URL**: `{{baseUrl}}/api/auth/login/`
- **Body** (JSON):
```json
{
  "email": "your@email.com",
  "password": "yourpassword"
}
```
- **Expected**: 200 OK with token

#### 3. Get Dashboard Data
- **Method**: GET
- **URL**: `{{baseUrl}}/api/accounts/dashboard/`
- **Auth**: Token (from login response)
- **Expected**: 200 OK with user data

## Testing from Frontend

### 1. Test API Service

Open browser console at `http://localhost:5173` and run:

```javascript
// Import the service (after logging in)
import { authService } from './services/authService';

// Test API connection
authService.testApi()
  .then(data => console.log('API Test:', data))
  .catch(error => console.error('API Test Failed:', error));

// Get dashboard data (requires authentication)
authService.getDashboard()
  .then(data => console.log('Dashboard:', data))
  .catch(error => console.error('Dashboard Fetch Failed:', error));
```

### 2. Check Network Tab

1. Open DevTools (F12)
2. Go to Network tab
3. Perform actions in the app
4. Check API requests/responses

## Common Issues & Solutions

### Issue: CORS Error

**Error**: 
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:5173' 
has been blocked by CORS policy
```

**Solution**: 
- Ensure `django-cors-headers` is installed
- Check `CORS_ALLOWED_ORIGINS` in settings.py includes `http://localhost:5173`
- Verify `CorsMiddleware` is in MIDDLEWARE list

### Issue: Authentication Required

**Error**: 
```
401 Unauthorized
```

**Solution**:
- Ensure you're logged in
- Check token is stored in localStorage
- Verify Authorization header is being sent

### Issue: Connection Refused

**Error**:
```
Failed to fetch
```

**Solution**:
- Check if Django server is running: `python manage.py runserver`
- Verify backend is on port 8000
- Check firewall settings

## Automated Testing

### Running Django Tests

```bash
cd backend
python manage.py test accounts
```

### Creating Test Cases

Create `accounts/tests.py`:

```python
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class APITestTestCase(APITestCase):
    def test_api_health(self):
        """Test the API health endpoint"""
        url = reverse('api_test')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')
        self.assertIn('message', response.data)
```

## Performance Testing

### Using Apache Bench

```bash
# Test API endpoint with 100 requests, 10 concurrent
ab -n 100 -c 10 http://localhost:8000/api/accounts/api-test/
```

### Expected Performance

- Health check: < 100ms
- Dashboard: < 200ms (authenticated)
- Login: < 300ms

## Security Testing

### Checklist

- [ ] CORS properly configured
- [ ] Authentication required for protected endpoints
- [ ] Token validation working
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF tokens in place
- [ ] Rate limiting (to be implemented)

## Monitoring API Usage

### Django Admin

1. Visit: http://localhost:8000/admin/
2. Login with superuser
3. Monitor:
   - User registrations
   - Token usage
   - Activity logs

### Django Debug Toolbar (Development)

Install:
```bash
pip install django-debug-toolbar
```

Add to `INSTALLED_APPS` and `MIDDLEWARE` in settings.py

## Next Steps

1. ✅ Test basic API endpoints
2. ✅ Verify frontend-backend connection
3. ⏳ Implement additional endpoints
4. ⏳ Add comprehensive tests
5. ⏳ Set up monitoring
6. ⏳ Configure production environment

---

**Last Updated**: March 6, 2026  
**API Version**: 1.0.0
