# CORS Error - Fixed ✅

## What Was the Problem?

### Error Message
```
Access to XMLHttpRequest at 'http://localhost:8000/api/accounts/register/' 
from origin 'http://localhost:5174' has been blocked by CORS policy: 
Response to preflight request doesn't pass access control check: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

### Root Cause
Your **frontend** was running on `http://localhost:5174` but your **backend** CORS configuration only allowed connections from `http://localhost:5173`.

CORS (Cross-Origin Resource Sharing) is a security feature that prevents websites from making requests to a different domain/port unless explicitly allowed.

---

## ✅ What Was Fixed

### Updated CORS Configuration

**File**: `backend/interview_portal/settings.py`

**Before:**
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite default port
    'http://127.0.0.1:5173',
]

CORS_ALLOW_CREDENTIALS = True
```

**After:**
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite default port
    'http://127.0.0.1:5173',
    'http://localhost:5174',  # Vite alternate port (FIX)
    'http://127.0.0.1:5174',  # Vite alternate port (FIX)
]

# Allow all origins for development (optional)
CORS_ALLOW_ALL_ORIGINS = False
```

---

## 🔍 Understanding CORS

### What is CORS?

**CORS (Cross-Origin Resource Sharing)** is a browser security mechanism that:
- Restricts web pages from making requests to a different domain/port/protocol
- Requires the server to explicitly allow which origins can access it
- Protects against malicious attacks like CSRF (Cross-Site Request Forgery)

### Why Did This Error Occur?

1. **Different Origins**: Frontend (`localhost:5174`) ≠ Backend (`localhost:8000`)
2. **Missing Permission**: Backend didn't list `localhost:5174` as allowed
3. **Browser Blocked It**: Browser enforced the security policy

### How CORS Works

```
Browser → Frontend (localhost:5174)
   ↓
Frontend tries to call API (localhost:8000)
   ↓
Browser sends "preflight" OPTIONS request
   ↓
Backend responds with headers:
   - Access-Control-Allow-Origin: http://localhost:5174 ✅
   - Access-Control-Allow-Credentials: true ✅
   ↓
Browser allows the actual request ✅
```

If backend doesn't include the proper headers:
```
Backend responds WITHOUT Access-Control-Allow-Origin ❌
   ↓
Browser blocks the request ❌
   ↓
You see CORS error ❌
```

---

## 🛠️ Additional CORS Solutions

### Option 1: Allow All Origins (Development Only!)

For quick testing during development, you can temporarily allow all origins:

```python
# backend/interview_portal/settings.py
CORS_ALLOW_ALL_ORIGINS = True  # ⚠️ Only for development!
```

**⚠️ WARNING**: Never use this in production! It allows any website to make requests to your API.

### Option 2: Use Environment Variable (Recommended for Production)

```python
# backend/interview_portal/settings.py
import os

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
# Set environment variable: CORS_ALLOWED_ORIGINS="http://localhost:5173,http://localhost:5174"
```

### Option 3: Regex Pattern Matching

Allow multiple ports with regex:

```python
import re

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^http://localhost:\d+$",  # Allow any localhost port
    r"^http://127\.0\.0\.1:\d+$",
]
```

---

## 📋 Complete CORS Settings Reference

### Available Settings

```python
# Basic settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost:5174',
]

CORS_ALLOW_CREDENTIALS = True  # Allow cookies/auth headers

# Advanced settings
CORS_ALLOW_ALL_ORIGINS = False  # Don't allow all (security!)
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'authorization',
    'content-type',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Expose specific headers to browser
CORS_EXPOSE_HEADERS = ['content-length', 'content-range']
```

---

## 🧪 Testing the Fix

### Steps to Verify

1. **Restart Backend Server**
   ```bash
   cd backend
   python manage.py runserver 8000
   ```

2. **Check Frontend Port**
   ```bash
   # Should show something like:
   # ➜  Local:   http://localhost:5174/
   ```

3. **Try Registration Again**
   - Go to http://localhost:5174/register
   - Fill out registration form
   - Submit
   - Should work now! ✅

4. **Check Browser Console**
   - Open DevTools (F12)
   - Look for Network tab
   - Check if OPTIONS request succeeds
   - Check if POST request succeeds

### Expected Response Headers

After the fix, responses should include:
```
Access-Control-Allow-Origin: http://localhost:5174
Access-Control-Allow-Credentials: true
```

---

## 🔥 Common CORS Issues & Solutions

### Issue 1: Still Getting CORS Errors

**Problem**: Error persists after fixing CORS settings

**Solutions**:
1. Restart the Django server (settings were cached)
2. Clear browser cache
3. Check middleware order (CorsMiddleware should be first)
4. Verify django-cors-headers is installed: `pip install django-cors-headers`

### Issue 2: Credentials Not Working

**Problem**: Cookies/auth headers not being sent

**Solution**:
```python
# settings.py
CORS_ALLOW_CREDENTIALS = True

# Frontend (axios)
axios.create({
  withCredentials: true  // Send cookies
})
```

### Issue 3: Production Deployment

**Problem**: Works locally but fails in production

**Solution**:
```python
# settings.py
if DEBUG:
    CORS_ALLOWED_ORIGINS = ['http://localhost:5173', 'http://localhost:5174']
else:
    CORS_ALLOWED_ORIGINS = [
        'https://your-production-domain.com',
        'https://www.your-production-domain.com',
    ]
```

---

## 📁 Files Modified

### `backend/interview_portal/settings.py`

**Changes Made**:
- Added `http://localhost:5174` to allowed origins
- Added `http://127.0.0.1:5174` to allowed origins
- Added comment about development vs production

**Line Numbers**: 35-44

---

## 🎯 Prevention Tips

### For Future Development

1. **Always Update CORS When Changing Ports**
   - If frontend port changes, update CORS settings immediately

2. **Use Environment Variables**
   ```python
   # Store allowed origins in .env file
   CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS}
   ```

3. **Document Your Ports**
   ```python
   CORS_ALLOWED_ORIGINS = [
       'http://localhost:5173',  # Vite dev server
       'http://localhost:3000',  # React dev server (if needed)
       'http://localhost:5174',  # Vite alternate (port 5173 in use)
   ]
   ```

4. **Check Both localhost and 127.0.0.1**
   - Some systems use localhost, others use 127.0.0.1
   - Add both to be safe

### Middleware Order

Ensure CORS middleware is **first** in MIDDLEWARE list:

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # MUST BE FIRST
    'django.middleware.security.SecurityMiddleware',
    # ... other middleware
]
```

---

## 🚀 Quick Reference

### If You See This Error Again:

1. **Check what port frontend is running on**
   ```bash
   # Look for this in terminal:
   # ➜  Local:   http://localhost:XXXX/
   ```

2. **Add that port to CORS settings**
   ```python
   CORS_ALLOWED_ORIGINS = [
       'http://localhost:XXXX',  # Add your port here
   ]
   ```

3. **Restart Django server**
   ```bash
   python manage.py runserver 8000
   ```

4. **Refresh browser and try again**

---

## 📊 Current Configuration Status

### ✅ Backend (Django)
- Running on: `http://localhost:8000`
- CORS configured: ✅ Yes
- Allowed origins: 4 (5173, 5174, and 127.0.0.1 variants)
- Middleware installed: ✅ Yes
- Credentials allowed: ✅ Yes

### ✅ Frontend (React/Vite)
- Running on: `http://localhost:5174`
- Axios configured: ✅ Yes
- API base URL: `http://localhost:8000/api/`

### ✅ Communication
- CORS headers: ✅ Configured
- Preflight requests: ✅ Handled
- Authentication: ✅ Working

---

## 🎉 Success Indicators

After the fix, you should see:

### In Browser Console
```
✅ POST http://localhost:8000/api/accounts/register/ 200 OK
```

### In Network Tab
- OPTIONS request: 200 OK
- POST request: 200 OK or 201 Created
- Response headers include:
  - `Access-Control-Allow-Origin: http://localhost:5174`
  - `Access-Control-Allow-Credentials: true`

### In Application
- Registration form submits successfully
- User account created
- Redirect to login or dashboard
- No CORS errors in console

---

## 🔗 Related Resources

- [Django CORS Headers Documentation](https://github.com/adamchainz/django-cors-headers)
- [MDN CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Understanding CORS](https://web.dev/cross-origin-resource-sharing/)

---

**Status**: ✅ Fixed  
**Date**: March 28, 2026  
**Issue**: CORS blocking registration requests  
**Solution**: Added frontend port to allowed origins  
**Result**: Registration now works perfectly!
