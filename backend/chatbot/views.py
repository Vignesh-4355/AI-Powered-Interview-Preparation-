from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.utils import timezone
import re
from .models import ChatMessage
from .serializers import ChatMessageSerializer, ChatRequestSerializer


class ChatbotView(views.APIView):
    """
    AI Chatbot endpoint with rule-based NLP
    
    POST /api/chatbot/
    Body: { "message": "user's message", "session_id": "optional" }
    
    Responses based on keywords and patterns in:
    - Interview preparation tips
    - Coding guidance
    - Company preparation
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_message = serializer.validated_data['message']
        session_id = serializer.validated_data.get('session_id', '')
        
        # Generate response using rule-based NLP
        response_text, category = self.generate_response(user_message)
        
        # Save to database
        ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            message=user_message,
            response=response_text,
            category=category,
            session_id=session_id
        )
        
        return Response({
            'message': user_message,
            'response': response_text,
            'category': category,
            'timestamp': timezone.now().isoformat(),
            'suggestions': self.get_suggestions(category, user_message)
        })

    def get_suggestions(self, category, message):
        """Get quick action suggestions based on context"""
        suggestions_map = {
            'Interview Prep': [
                'Common interview questions',
                'How to handle interview anxiety',
                'Technical interview tips',
                'STAR method explanation'
            ],
            'Coding': [
                'Best platforms to practice coding',
                'How to improve problem-solving',
                'Important data structures',
                'Dynamic programming tips'
            ],
            'Company': [
                'TCS interview preparation',
                'Amazon interview process',
                'Google interview tips',
                'Service vs product companies'
            ],
            'Resume': [
                'Resume formatting tips',
                'How to write achievements',
                'Projects to include',
                'Resume keywords'
            ],
            'General': [
                'Interview preparation tips',
                'Coding guidance',
                'Company preparation',
                'Resume building advice'
            ]
        }
        
        return suggestions_map.get(category, suggestions_map['General'])

    def generate_response(self, message):
        """Rule-based NLP to generate responses"""
        message_lower = message.lower()
        
        # Interview Preparation keywords
        interview_patterns = [
            r'interview\s*(preparation|tips|prepare)',
            r'how\s*to\s*(pass|clear|crack)\s*interview',
            r'interview\s*(anxiety|nervous|scared)',
            r'common\s*interview\s*questions',
            r'behavioral\s*interview',
            r'technical\s*interview',
        ]
        
        if any(re.search(pattern, message_lower) for pattern in interview_patterns):
            return self._get_interview_tips(message_lower), 'Interview Prep'
        
        # Coding guidance keywords
        coding_patterns = [
            r'(coding|programming|algorithm|data\s*structure)',
            r'(python|java|javascript|cpp|c\+\+)',
            r'(leetcode|hackerrank|codeforces)',
            r'(array|linked\s*list|tree|graph|dp|dynamic\s*programming)',
            r'(sorting|searching|recursion)',
            r'how\s*to\s*improve\s*coding\s*skills',
        ]
        
        if any(re.search(pattern, message_lower) for pattern in coding_patterns):
            return self._get_coding_guidance(message_lower), 'Coding'
        
        # Company preparation keywords
        company_patterns = [
            r'(company|companies)\s*(preparation|specific)',
            r'(tcs|infosys|wipro|amazon|google|microsoft|facebook)',
            r'company\s*interview\s*pattern',
            r'which\s*company.*better',
            r'company.*culture',
        ]
        
        if any(re.search(pattern, message_lower) for pattern in company_patterns):
            return self._get_company_prep(message_lower), 'Company'
        
        # Resume tips
        resume_patterns = [
            r'resume.*(tip|review|build|create|improve)',
            r'cv.*(help|guide|format)',
            r'how\s*to\s*make\s*resume',
        ]
        
        if any(re.search(pattern, message_lower) for pattern in resume_patterns):
            return self._get_resume_tips(message_lower), 'Resume'
        
        # Default/general conversation
        return self._get_general_response(message_lower), 'General'

    def _get_interview_tips(self, message):
        """Generate interview preparation tips"""
        tips = {
            'preparation': "For interview preparation:\n\n1. Research the company thoroughly\n2. Practice common interview questions\n3. Prepare STAR method stories (Situation, Task, Action, Result)\n4. Dress professionally\n5. Arrive 10-15 minutes early\n6. Bring multiple copies of your resume\n\nWould you like specific tips on any of these?",
            
            'anxiety': "Interview anxiety is normal! Here's how to manage it:\n\n1. Practice deep breathing exercises\n2. Prepare and rehearse answers\n3. Visualize success\n4. Remember: interviews are conversations, not interrogations\n5. Focus on what you can control\n\nYou've got this! 💪",
            
            'questions': "Common interview questions include:\n\n1. Tell me about yourself\n2. What are your strengths/weaknesses?\n3. Why do you want to work here?\n4. Describe a challenging situation\n5. Where do you see yourself in 5 years?\n\nPractice answering these with the STAR method!",
            
            'technical': "For technical interviews:\n\n1. Master data structures & algorithms\n2. Practice coding problems daily\n3. Explain your thought process aloud\n4. Ask clarifying questions\n5. Test your code with examples\n6. Optimize for time/space complexity\n\nConsistent practice is key!",
        }
        
        for key, tip in tips.items():
            if key in message:
                return tip
        
        return "Interview preparation is crucial! Here are key tips:\n\n✅ Research the company culture and values\n✅ Practice answering common questions\n✅ Prepare thoughtful questions to ask them\n✅ Do mock interviews with friends\n✅ Review the job description carefully\n✅ Prepare STAR method stories\n\nWhat specific aspect would you like help with?"

    def _get_coding_guidance(self, message):
        """Generate coding guidance"""
        if 'python' in message:
            return "Python tips for interviews:\n\n1. Master list comprehensions\n2. Understand decorators and generators\n3. Know built-in functions (map, filter, reduce)\n4. Practice with libraries like collections, itertools\n5. Learn time complexity of operations\n\nPractice platforms: LeetCode, HackerRank, CodeSignal"
        
        if 'java' in message:
            return "Java interview preparation:\n\n1. OOP concepts (inheritance, polymorphism, encapsulation)\n2. Collections framework (HashMap, ArrayList)\n3. Multithreading basics\n4. Exception handling\n5. Java 8 features (streams, lambdas)\n\nFocus on problem-solving patterns!"
        
        if 'algorithm' in message or 'data structure' in message:
            return "Essential DSA topics:\n\n📚 Arrays & Strings (most common)\n📚 Linked Lists\n📚 Trees & Graphs\n📚 Dynamic Programming\n📚 Sorting & Searching\n📚 Hash Tables\n\nStart with easy problems, then medium. Quality > Quantity!"
        
        if 'improve' in message:
            return "To improve coding skills:\n\n1. Code daily (even 30 mins helps)\n2. Solve problems slightly above your level\n3. Read others' solutions\n4. Build projects\n5. Contribute to open source\n6. Learn design patterns\n7. Practice explaining your code\n\nConsistency is more important than intensity!"
        
        return "Coding guidance I can provide:\n\n💻 Language-specific tips (Python, Java, JavaScript, C++)\n💻 Data structures & algorithms\n💻 Problem-solving strategies\n💻 Best practices & clean code\n💻 Project ideas\n\nWhat specific topic would you like to explore?"

    def _get_company_prep(self, message):
        """Generate company preparation advice"""
        if 'amazon' in message:
            return "Amazon interview prep:\n\n🎯 Focus on Leadership Principles (14 LPs)\n🎯 Prepare STAR stories for each LP\n🎯 Technical: DSA + System Design\n🎯 Behavioral round is crucial\n🎯 Think customer-first in all answers\n\nResearch their recent news and products!"
        
        if 'google' in message:
            return "Google interview prep:\n\n🎯 Strong DSA fundamentals required\n🎯 Practice medium-hard LeetCode problems\n🎯 System design for experienced roles\n🎯 Googleyness (culture fit) matters\n🎯 Mock interviews essential\n\nAverage prep time: 2-3 months"
        
        if 'microsoft' in message:
            return "Microsoft interview prep:\n\n🎯 DSA + Problem solving\n🎯 System design basics\n🎯 Cultural fit assessment\n🎯 Know Microsoft products\n🎯 Growth mindset is valued\n\nThey value learning ability over perfection!"
        
        if 'tcs' in message or 'infosys' in message or 'wipro' in message:
            return "Service-based company prep:\n\n🎯 Aptitude: Quantitative, Logical, Verbal\n🎯 Basic coding fundamentals\n🎯 Communication skills important\n🎯 HR questions about relocation, shifts\n🎯 Know company's recent projects\n\nFocus on speed and accuracy in aptitude!"
        
        return "Company preparation strategy:\n\n✅ Research company mission & values\n✅ Study recent news & products\n✅ Understand role requirements\n✅ Prepare why this company specifically\n✅ Network with current employees\n✅ Practice company-specific interview patterns\n\nWhich company are you targeting? I can give specific advice!"

    def _get_resume_tips(self, message):
        """Generate resume tips"""
        return "Resume best practices:\n\n📄 Keep it 1 page (max 2 for experienced)\n📄 Use action verbs (developed, implemented, led)\n📄 Quantify achievements (increased X by Y%)\n📄 Tailor for each job application\n📄 Include projects & technologies\n📄 No spelling/grammar errors\n📄 Use clean, professional format\n\nWant tips on any specific section?"

    def _get_general_response(self, message):
        """Generate general responses"""
        greetings = ['hi', 'hello', 'hey', 'greetings']
        
        if any(greet in message for greet in greetings):
            return "Hello! 👋 I'm your AI interview assistant. I can help you with:\n\n• Interview preparation tips\n• Coding guidance & DSA\n• Company-specific preparation\n• Resume building advice\n\nWhat would you like to know?"
        
        if 'thank' in message:
            return "You're welcome! 😊 Feel free to ask anything else about interview preparation, coding, companies, or resumes. I'm here to help!"
        
        if 'bye' in message or 'goodbye' in message:
            return "Good luck with your interview preparation! 🍀 Feel free to come back anytime you need assistance. You've got this!"
        
        return "Thanks for your message! I specialize in helping with:\n\n🎯 Interview preparation strategies\n🎯 Coding & DSA guidance\n🎯 Company-specific tips\n🎯 Resume building advice\n\nCould you please be more specific about what you'd like help with?"
