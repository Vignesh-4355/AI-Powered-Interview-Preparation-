# Resume Analyzer - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Start the Servers

**Backend:**
```bash
cd backend
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Or use the startup script:
```bash
start.bat
```

### Step 2: Access the Feature

1. Open browser to **http://localhost:5174** (or your frontend URL)
2. Login/Register
3. Click **"Resume Analyzer"** from Dashboard
4. Or navigate directly to **http://localhost:5174/resume-analyzer**

### Step 3: Upload Your Resume

1. **Drag & drop** your PDF resume OR click "Browse Files"
2. Click **"Analyze Resume"**
3. Wait 2-5 seconds for analysis
4. Review comprehensive results!

---

## 📊 What You'll Get

### Analysis Results Include:

#### **Three Key Scores**
- 🎯 **Skill Score** - Technical skill strength (0-100)
- 📄 **Formatting Score** - Structure quality (0-100)
- 🤖 **ATS Score** - Applicant Tracking System compatibility (0-100)

#### **Skills Breakdown**
- ✅ **Detected Skills** - All technical skills found
- ⚠️ **Missing Skills** - Important skills to add
- 📈 **Top Keywords** - Most frequent ATS keywords

#### **Actionable Feedback**
- 💪 **Strengths** - What you're doing right
- 🔧 **Areas for Improvement** - What needs work
- 💡 **Suggestions** - Specific recommendations
- ❌ **ATS Issues** - Compatibility problems

---

## 🎨 Understanding the UI

### Color Coding
- 🟢 **Green** (80-100) - Excellent
- 🟠 **Orange** (60-79) - Good, needs improvement
- 🔴 **Red** (0-59) - Needs attention

### Skill Tags
- **Green border** - Detected in your resume
- **Orange border** - Missing (priority indicated)

### Progress Bars
- Show keyword density visually
- Longer bar = higher frequency

---

## 💡 Tips for Best Results

### Before Uploading
1. ✅ Save resume as PDF
2. ✅ Ensure file size < 10MB
3. ✅ Use standard section headings
4. ✅ Include contact information

### After Analysis
1. 📝 Review all suggestions
2. ✏️ Update your resume
3. 🔄 Re-upload improved version
4. 📊 Compare scores

---

## 🎯 Improve Your Score

### Quick Wins (+10-15 points each)
- Add a "Skills" section
- Include phone number and email
- Use "Experience" and "Education" headings
- Add GitHub/LinkedIn profiles

### Medium Impact (+5-10 points each)
- List 5+ technical skills
- Mention specific technologies
- Quantify achievements with numbers
- Use action verbs

### Long-term Strategy (+20-30 points)
- Learn missing high-priority skills
- Add relevant projects
- Include certifications
- Expand technical skill set

---

## 📱 Mobile Support

The Resume Analyzer is fully responsive! Works on:
- 📱 Smartphones
- 📱 Tablets
- 💻 Laptops
- 🖥️ Desktops

---

## 🔍 Example Analysis

### Sample Input
```
File: john_doe_resume.pdf
Size: 245 KB
Pages: 2
```

### Sample Output
```
📊 Scores:
   Skill Score: 75/100 ✅
   Formatting: 85/100 ✅
   ATS Score: 70/100 ⚠️

✅ Detected Skills (12):
   Python, Java, React, Django, SQL, AWS, Docker, Git...

⚠️ Missing Skills (3):
   JavaScript (High Priority)
   TypeScript (Medium Priority)
   Kubernetes (Medium Priority)

💡 Suggestions:
   - Add JavaScript explicitly to skills section
   - Include phone number for ATS compatibility
   - Quantify project impacts with metrics
   - Use standard section headings
```

---

## ❓ FAQ

**Q: What file formats are accepted?**  
A: Only PDF files, max 10MB.

**Q: How long does analysis take?**  
A: Typically 2-5 seconds.

**Q: Can I upload multiple resumes?**  
A: Yes! View history to see all uploads.

**Q: Is my resume data private?**  
A: Yes, only you can see your resumes.

**Q: Why is my ATS score low?**  
A: Check for missing sections, contact info, and standard headings.

**Q: How can I improve my skill score?**  
A: Add more technical skills from different categories.

---

## 🎉 Ready to Optimize Your Resume?

Start analyzing now at **http://localhost:5174/resume-analyzer**

Good luck! 🚀
