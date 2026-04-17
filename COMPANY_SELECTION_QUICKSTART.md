# Company Selection Module - Quick Start Guide

## 🚀 Quick Setup

### Step 1: Verify Backend is Running

```bash
cd backend
python manage.py runserver 8000
```

### Step 2: Populate Sample Data (if not already done)

```bash
cd backend
python manage.py populate_sample_companies
```

You should see:
```
✓ Created company: Microsoft
✓ Created company: Google
✓ Created company: Accenture
...
✓ Successfully created 10 companies!
```

### Step 3: Access the Page

1. Login to your account
2. Go to Dashboard
3. Click "Company Specific Preparation"
4. OR visit: http://localhost:5174/companies-list

---

## 📋 What You'll See

### Company Grid
- **10 Companies** displayed as beautiful cards
- **3-4 cards per row** on desktop
- **Responsive** - adjusts for mobile/tablet

### Each Card Shows:
- 🏢 Company logo
- 📛 Company name
- 🏷️ Industry tag
- 📝 Short description
- 🎯 Difficulty badge (Easy/Medium/Hard)
- 📚 Total questions count
- 📈 Hiring frequency
- 🔘 "Prepare Now" button

### Search & Filter
- 🔍 **Search bar** - Type to search companies
- 🎚️ **Difficulty filter** - Easy/Medium/Hard/All

---

## 🎮 How to Use

### Browse Companies
- Scroll through the grid
- View company details on each card
- Check difficulty level and question count

### Search for a Company
1. Click on search bar
2. Type company name or industry
3. Results filter in real-time
4. Example: "Amazon", "IT Services", "Technology"

### Filter by Difficulty
1. Click difficulty dropdown
2. Select Easy, Medium, or Hard
3. Grid updates immediately
4. Combine with search for precise results

### Start Preparation
1. Click any company card
2. OR click "Prepare Now" button
3. You'll navigate to company detail page
4. Access interview patterns and questions

---

## 🎯 Companies Available

| Company | Difficulty | Questions | Hiring |
|---------|-----------|-----------|--------|
| **TCS** | Easy | 250 | High |
| **Infosys** | Easy | 230 | High |
| **Wipro** | Easy | 200 | High |
| **Cognizant** | Easy | 220 | High |
| **Accenture** | Medium | 300 | High |
| **Deloitte** | Medium | 280 | Medium |
| **IBM** | Medium | 350 | Medium |
| **Amazon** | Hard | 450 | Medium |
| **Microsoft** | Hard | 500 | Medium |
| **Google** | Hard | 600 | Low |

---

## 🎨 UI Features

### Hover Effects
- Card lifts up slightly
- Shadow appears
- Gradient border on top
- Smooth animation

### Color Coding
- 🟢 **Green** = Easy difficulty
- 🟡 **Yellow** = Medium difficulty
- 🔴 **Red** = Hard difficulty

### Responsive Design
- 📱 **Mobile**: 1 card per row
- 📱 **Tablet**: 2-3 cards per row
- 💻 **Desktop**: 3-4 cards per row

---

## 🔧 Troubleshooting

### No Companies Showing?
1. Check backend is running
2. Run: `python manage.py populate_sample_companies`
3. Refresh the page

### Search Not Working?
1. Check browser console for errors
2. Verify API is responding
3. Try: http://localhost:8000/api/companies/

### Images Not Loading?
- Logos are loaded from Clearbit API
- May be blocked by ad blockers
- Fallback icon displays if logo fails

---

## 📍 Navigation Flow

```
Dashboard
    ↓
Click "Company Specific Preparation"
    ↓
Company List Page (/companies-list)
    ↓
Search/Filter companies
    ↓
Click company card
    ↓
Company Detail Page (/company/{id})
    ↓
View patterns & questions
```

---

## 🎯 Next Steps

After selecting a company:
1. ✅ View interview patterns
2. ✅ Browse company-specific questions
3. ✅ Filter by question type (HR/Tech/Coding)
4. ✅ Practice with detailed answers
5. ✅ Watch video explanations

---

## 💡 Pro Tips

1. **Start with Easy** - If you're a beginner, start with TCS/Infosys
2. **Use Search** - Quickly find specific companies
3. **Check Difficulty** - Match questions to your skill level
4. **View Hiring** - High hiring companies = more opportunities
5. **Explore Patterns** - Understand each company's interview process

---

## 📞 Need Help?

- Check browser console for errors
- Verify both servers are running
- Review API documentation
- Check CORS settings if needed

---

**Ready to Start?** 🚀

Visit: http://localhost:5174/companies-list
