from rest_framework import views, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Avg
from .models import Resume, ResumeAnalysis
from .serializers import ResumeSerializer, ResumeAnalysisSerializer
from pypdf import PdfReader
import re
from collections import Counter


# Common tech skills and keywords database
TECH_SKILLS = {
    'Programming Languages': [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust', 
        'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB'
    ],
    'Web Technologies': [
        'React', 'Angular', 'Vue', 'Django', 'Flask', 'FastAPI', 'Node.js', 
        'Express', 'Spring Boot', 'HTML', 'CSS', 'SASS', 'Tailwind', 'Bootstrap'
    ],
    'Databases': [
        'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch', 
        'Oracle', 'SQLite', 'Firebase', 'DynamoDB'
    ],
    'DevOps & Cloud': [
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'CI/CD', 
        'Terraform', 'Ansible', 'Linux', 'Git', 'GitHub', 'GitLab'
    ],
    'Tools & Frameworks': [
        'TensorFlow', 'PyTorch', 'Pandas', 'NumPy', 'Scikit-learn', 'REST API', 
        'GraphQL', 'Microservices', 'Agile', 'Scrum'
    ]
}

# Important keywords for ATS
ATS_KEYWORDS = [
    'experience', 'skills', 'education', 'project', 'development', 'design',
    'implementation', 'management', 'analysis', 'testing', 'deployment',
    'optimization', 'collaboration', 'leadership', 'architecture', 'system'
]

# Common formatting issues
FORMATTING_ISSUES = {
    'too_short': {'min_words': 200, 'message': 'Resume might be too short'},
    'too_long': {'max_words': 1500, 'message': 'Resume might be too long'},
    'missing_sections': ['email', 'phone', 'education', 'experience'],
}


class ResumeAnalyzerView(views.APIView):
    """API endpoint to analyze uploaded resume"""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        """Upload and analyze resume"""
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES['file']
        
        # Validate file type
        if not file.name.endswith('.pdf'):
            return Response(
                {'error': 'Only PDF files are accepted'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create Resume object
            resume = Resume.objects.create(
                user=request.user,
                file=file,
                original_filename=file.name,
                file_size=file.size
            )

            # Extract text from PDF
            extracted_text = self.extract_text_from_pdf(file)
            resume.extracted_text = extracted_text
            resume.save()

            # Analyze the resume
            analysis = self.analyze_resume(extracted_text, resume)

            return Response({
                'resume': ResumeSerializer(resume).data,
                'analysis': ResumeAnalysisSerializer(analysis).data,
                'message': 'Resume analyzed successfully!'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Failed to analyze resume: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF using pypdf"""
        try:
            pdf_file.seek(0)
            reader = PdfReader(pdf_file)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"PDF extraction failed: {str(e)}")

    def analyze_resume(self, text, resume):
        """Comprehensive resume analysis"""
        # Detect skills
        detected_skills = self.detect_skills(text)
        
        # Find missing skills
        missing_skills = self.find_missing_skills(detected_skills)
        
        # Extract keywords
        keywords_found = self.extract_keywords(text)
        
        # Calculate scores
        skill_score = self.calculate_skill_score(detected_skills)
        keyword_density = self.calculate_keyword_density(text, keywords_found)
        formatting_score = self.check_formatting(text)
        ats_score = self.calculate_ats_score(text, detected_skills)
        
        # Generate feedback
        strengths, weaknesses, suggestions = self.generate_feedback(
            text, detected_skills, missing_skills, skill_score, ats_score
        )
        
        # Identify ATS issues
        ats_issues = self.identify_ats_issues(text)

        # Create or update analysis
        analysis, _ = ResumeAnalysis.objects.get_or_create(resume=resume)
        analysis.detected_skills = detected_skills
        analysis.missing_skills = missing_skills
        analysis.keywords_found = keywords_found
        analysis.skill_score = skill_score
        analysis.keyword_density = keyword_density
        analysis.formatting_score = formatting_score
        analysis.strengths = strengths
        analysis.weaknesses = weaknesses
        analysis.suggestions = suggestions
        analysis.ats_score = ats_score
        analysis.ats_issues = ats_issues
        analysis.save()

        return analysis

    def detect_skills(self, text):
        """Detect technical skills in resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for category, skills in TECH_SKILLS.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.append({
                        'skill': skill,
                        'category': category
                    })
        
        return found_skills

    def find_missing_skills(self, detected_skills):
        """Identify important missing skills"""
        detected_set = {skill['skill'].lower() for skill in detected_skills}
        missing = []
        
        # Check each category for missing key skills
        for category, skills in TECH_SKILLS.items():
            category_detected = [s for s in detected_skills if s['category'] == category]
            
            # If less than 2 skills from a category, suggest some
            if len(category_detected) < 2 and category in ['Programming Languages', 'Web Technologies']:
                # Suggest top 3 most common skills not present
                for skill in skills[:3]:
                    if skill.lower() not in detected_set:
                        missing.append({
                            'skill': skill,
                            'category': category,
                            'priority': 'High' if category == 'Programming Languages' else 'Medium'
                        })
        
        return missing

    def extract_keywords(self, text):
        """Extract important keywords from resume"""
        words = re.findall(r'\b\w{4,}\b', text.lower())
        word_counts = Counter(words)
        
        # Filter for ATS keywords
        found_keywords = []
        for keyword in ATS_KEYWORDS:
            if keyword in word_counts:
                found_keywords.append({
                    'keyword': keyword,
                    'count': word_counts[keyword],
                    'density': round((word_counts[keyword] / len(words)) * 100, 2)
                })
        
        return sorted(found_keywords, key=lambda x: x['count'], reverse=True)[:15]

    def calculate_skill_score(self, detected_skills):
        """Calculate overall skill score (0-100)"""
        total_categories = len(TECH_SKILLS)
        categories_covered = len(set(skill['category'] for skill in detected_skills))
        
        # Base score from category coverage
        coverage_score = (categories_covered / total_categories) * 60
        
        # Bonus for number of skills
        skill_bonus = min(len(detected_skills) * 3, 40)
        
        return min(round(coverage_score + skill_bonus, 2), 100)

    def calculate_keyword_density(self, text, keywords):
        """Calculate keyword density percentage"""
        words = text.split()
        total_keywords = sum(kw['count'] for kw in keywords)
        
        if not words:
            return 0
        
        return round((total_keywords / len(words)) * 100, 2)

    def check_formatting(self, text):
        """Check resume formatting quality"""
        score = 100
        words = text.split()
        word_count = len(words)
        
        # Check length
        if word_count < FORMATTING_ISSUES['too_short']['min_words']:
            score -= 20
        elif word_count > FORMATTING_ISSUES['too_long']['max_words']:
            score -= 15
        
        # Check for sections
        text_lower = text.lower()
        for section in FORMATTING_ISSUES['missing_sections']:
            if section not in text_lower:
                score -= 10
        
        return max(score, 0)

    def calculate_ats_score(self, text, detected_skills):
        """Calculate ATS compatibility score"""
        score = 100
        text_lower = text.lower()
        
        # Check for standard sections
        standard_sections = ['experience', 'education', 'skills', 'project']
        for section in standard_sections:
            if section not in text_lower:
                score -= 15
        
        # Bonus for having detected skills
        if len(detected_skills) >= 10:
            score += 10
        elif len(detected_skills) >= 5:
            score += 5
        
        # Check for contact info
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            score -= 15
        
        return max(min(score, 100), 0)

    def generate_feedback(self, text, detected_skills, missing_skills, skill_score, ats_score):
        """Generate actionable feedback"""
        strengths = []
        weaknesses = []
        suggestions = []

        # Strengths
        if skill_score >= 70:
            strengths.append("Strong technical skill set")
        if len(detected_skills) >= 15:
            strengths.append("Good variety of technologies mentioned")
        if ats_score >= 80:
            strengths.append("Well-formatted for ATS systems")

        # Weaknesses
        if skill_score < 50:
            weaknesses.append("Limited technical skills detected")
        if ats_score < 60:
            weaknesses.append("ATS compatibility issues detected")
        if len(missing_skills) > 5:
            weaknesses.append("Several key skills missing")

        # Suggestions
        if missing_skills:
            top_missing = missing_skills[0]['skill'] if missing_skills else ''
            suggestions.append(f"Consider adding {top_missing} to your resume")
        
        if skill_score < 60:
            suggestions.append("Highlight more technical projects and technologies")
        
        if ats_score < 70:
            suggestions.append("Use standard section headings like 'Experience' and 'Education'")
        
        suggestions.append("Quantify achievements with numbers and metrics")
        suggestions.append("Use action verbs to describe responsibilities")

        return strengths, weaknesses, suggestions

    def identify_ats_issues(self, text):
        """Identify specific ATS compatibility issues"""
        issues = []
        text_lower = text.lower()
        
        # Check for standard sections
        if 'experience' not in text_lower:
            issues.append("Missing 'Experience' section")
        if 'education' not in text_lower:
            issues.append("Missing 'Education' section")
        if 'skills' not in text_lower:
            issues.append("Missing 'Skills' section")
        
        # Check for contact info
        if not re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text):
            issues.append("Phone number not detected")
        if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            issues.append("Email address not detected")
        
        # Check for URLs
        if 'github' not in text_lower and 'linkedin' not in text_lower:
            issues.append("Consider adding GitHub or LinkedIn profile")
        
        return issues


class ResumeHistoryView(views.APIView):
    """Get user's resume upload history"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get all resumes for authenticated user"""
        resumes = Resume.objects.filter(user=request.user)
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)


class ResumeDetailView(views.APIView):
    """Get detailed analysis of a specific resume"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, resume_id):
        """Get resume details and analysis"""
        try:
            resume = Resume.objects.get(id=resume_id, user=request.user)
            
            # Get or create analysis
            analysis, _ = ResumeAnalysis.objects.get_or_create(resume=resume)
            
            return Response({
                'resume': ResumeSerializer(resume).data,
                'analysis': ResumeAnalysisSerializer(analysis).data
            })
        except Resume.DoesNotExist:
            return Response(
                {'error': 'Resume not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
