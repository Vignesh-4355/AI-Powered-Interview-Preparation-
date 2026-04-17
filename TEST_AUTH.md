# 🧪 Testing Authentication System

## Quick Test Guide

### 1. Test Registration via Browser Console

Open your browser console (F12) at http://localhost:5173/register and run:

```javascript
// Test registration data
const testData = {
  email: 'test@example.com',
  password: 'testpassword123',
  password_confirm: 'testpassword123',
  first_name: 'Test',
  last_name: 'User'
};

console.log('Testing registration with:', testData);

// Make the API call directly
fetch('http://localhost:8000/api/accounts/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(testData)
})
.then(response => {
  console.log('Status:', response.status);
  return response.json();
})
.then(data => {
  console.log('Response:', data);
  if (data.access_token) {
    console.log('✅ Registration successful!');
    console.log('Token:', data.access_token);
  } else {
    console.log('❌ Registration failed:', data);
  }
})
.catch(error => {
  console.error('❌ Error:', error);
});
```

### 2. Test Login via Browser Console

```javascript
// Test login
fetch('http://localhost:8000/api/accounts/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'test@example.com',
    password: 'testpassword123'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Login response:', data);
  if (data.access_token) {
    console.log('✅ Login successful!');
    console.log('Token:', data.access_token);
  } else {
    console.log('❌ Login failed:', data);
  }
})
.catch(error => console.error('❌ Error:', error));
```

### 3. Test API Health

Visit in browser: http://localhost:8000/api/accounts/api-test/

Expected response:
```json
{
  "message": "AI Powered Interview Preparation Portal API is running!",
  "version": "1.0.0",
  "status": "healthy"
}
```

### 4. Check Backend Logs

Watch the terminal where backend is running for error messages.

### 5. Common Issues & Solutions

#### Issue: "Registration failed with status 500"

**Solution**: Check backend terminal for detailed error message

#### Issue: "Cannot read properties of undefined"

**Solution**: 
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Check browser console for errors

#### Issue: "CORS error"

**Solution**: Verify CORS settings in `backend/interview_portal/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
```

#### Issue: "ModuleNotFoundError: No module named 'accounts.serializers'"

**Solution**: ✅ Already fixed - serializers.py file created

### 6. Manual Database Check

If registration still fails, check if user already exists:

```bash
cd backend
python manage.py shell
```

Then in Python shell:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
print("All users:", list(User.objects.all().values_list('email', flat=True)))
```

### 7. Create Superuser Manually

```bash
cd backend
python manage.py createsuperuser
```

Enter:
- Email: admin@example.com
- Password: adminpassword123

Then login at http://localhost:5173/login with these credentials.

---

## Expected Flow

1. ✅ Visit http://localhost:5173/register
2. ✅ Fill in form with valid data
3. ✅ Click "Create Account"
4. ✅ Should redirect to http://localhost:5173/dashboard
5. ✅ See welcome message with your email

---

## Debug Checklist

- [ ] Backend server running at http://localhost:8000
- [ ] Frontend server running at http://localhost:5173
- [ ] No errors in backend terminal
- [ ] Browser console open (F12)
- [ ] Network tab shows 200/201 status codes
- [ ] localStorage has access_token after registration

---

**Last Updated**: March 7, 2026  
**Status**: Ready for testing
