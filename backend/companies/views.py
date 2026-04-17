from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Company, CompanyInterviewPattern, CompanyQuestion
from .serializers import (
    CompanySerializer,
    CompanyListSerializer,
    CompanyInterviewPatternSerializer,
    CompanyQuestionSerializer
)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Company instances.
    
    Actions:
    - list: GET /api/companies/ - List all companies
    - retrieve: GET /api/companies/{id}/ - Get company details with patterns and questions
    - patterns: GET /api/companies/{id}/patterns/ - Get company interview patterns
    - questions: GET /api/companies/{id}/questions/ - Get company questions
    """
    queryset = Company.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access for now

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return CompanyListSerializer
        return CompanySerializer

    def get_queryset(self):
        """Optionally filter companies by search query"""
        queryset = Company.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    @action(detail=True, methods=['get'])
    def patterns(self, request, pk=None):
        """Get interview patterns for a specific company"""
        company = self.get_object()
        patterns = company.interview_patterns.all()
        serializer = CompanyInterviewPatternSerializer(patterns, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """Get questions for a specific company with optional filtering"""
        company = self.get_object()
        questions = company.questions.all()
        
        # Filter by question type if provided
        question_type = request.query_params.get('type', None)
        if question_type:
            questions = questions.filter(question_type=question_type)
        
        # Filter by difficulty if provided
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            questions = questions.filter(difficulty=difficulty)
        
        serializer = CompanyQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """Get complete company details including patterns and questions"""
        company = self.get_object()
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def strategy(self, request, pk=None):
        """Get preparation strategy for a specific company"""
        company = self.get_object()
        
        # Generate company-specific strategy based on difficulty
        strategies = {
            'Easy': {
                'weeks': 4,
                'plan': [
                    {
                        'week': 1,
                        'title': 'Foundation Building',
                        'tasks': [
                            'Practice aptitude questions (Quantitative, Logical, Verbal)',
                            'Revise basic programming concepts (Variables, Loops, Functions)',
                            'Learn company profile and values',
                            'Practice basic data structures (Arrays, Strings)'
                        ],
                        'hours_per_day': 3
                    },
                    {
                        'week': 2,
                        'title': 'Core Skills Development',
                        'tasks': [
                            'Solve 20+ coding problems (Easy level)',
                            'Practice SQL queries and database concepts',
                            'Study OOP concepts (Classes, Objects, Inheritance)',
                            'Mock aptitude tests (timed)'
                        ],
                        'hours_per_day': 4
                    },
                    {
                        'week': 3,
                        'title': 'Advanced Preparation',
                        'tasks': [
                            'Practice previous year questions',
                            'Study core CS subjects (OS, DBMS, Networks)',
                            'Prepare projects explanation',
                            'Practice group discussion topics'
                        ],
                        'hours_per_day': 4
                    },
                    {
                        'week': 4,
                        'title': 'Final Revision & Mock Interviews',
                        'tasks': [
                            'Take full-length mock tests',
                            'Revise all important concepts',
                            'Practice HR questions and answers',
                            'Mock technical interviews with peers'
                        ],
                        'hours_per_day': 5
                    }
                ]
            },
            'Medium': {
                'weeks': 6,
                'plan': [
                    {
                        'week': 1,
                        'title': 'Aptitude & Reasoning Mastery',
                        'tasks': [
                            'Advanced aptitude practice (Time & Work, Probability)',
                            'Logical reasoning puzzles',
                            'Verbal ability and comprehension',
                            'Data interpretation practice'
                        ],
                        'hours_per_day': 3
                    },
                    {
                        'week': 2,
                        'title': 'Programming Fundamentals',
                        'tasks': [
                            'Data structures (Arrays, Linked Lists, Stacks, Queues)',
                            'Algorithm basics (Sorting, Searching)',
                            'Practice 30+ easy coding problems',
                            'Time and space complexity analysis'
                        ],
                        'hours_per_day': 4
                    },
                    {
                        'week': 3,
                        'title': 'Core CS Subjects',
                        'tasks': [
                            'Operating Systems (Processes, Threads, Memory)',
                            'Database Management (SQL, Normalization, Transactions)',
                            'Computer Networks (TCP/IP, HTTP, DNS)',
                            'System Design basics'
                        ],
                        'hours_per_day': 4
                    },
                    {
                        'week': 4,
                        'title': 'Advanced DSA',
                        'tasks': [
                            'Trees and Graphs (BFS, DFS, Traversals)',
                            'Dynamic Programming basics',
                            'Recursion and Backtracking',
                            'Solve 40+ medium coding problems'
                        ],
                        'hours_per_day': 5
                    },
                    {
                        'week': 5,
                        'title': 'Projects & System Design',
                        'tasks': [
                            'Prepare detailed project explanations',
                            'Practice system design questions',
                            'Study company-specific technologies',
                            'Behavioral questions preparation'
                        ],
                        'hours_per_day': 4
                    },
                    {
                        'week': 6,
                        'title': 'Mock Interviews & Revision',
                        'tasks': [
                            'Daily mock interviews (Technical + HR)',
                            'Revise all concepts and formulas',
                            'Practice with company question bank',
                            'Final preparation and confidence building'
                        ],
                        'hours_per_day': 5
                    }
                ]
            },
            'Hard': {
                'weeks': 8,
                'plan': [
                    {
                        'week': 1,
                        'title': 'Advanced Aptitude & Problem Solving',
                        'tasks': [
                            'Complex quantitative problems',
                            'Advanced logical puzzles',
                            'Critical reasoning practice',
                            'Speed mathematics techniques'
                        ],
                        'hours_per_day': 3
                    },
                    {
                        'week': 2,
                        'title': 'Data Structures Deep Dive',
                        'tasks': [
                            'Advanced trees (BST, AVL, Segment Trees)',
                            'Graph algorithms (Dijkstra, MST, Topological Sort)',
                            'Heaps and Priority Queues',
                            'Hash tables and implementations'
                        ],
                        'hours_per_day': 5
                    },
                    {
                        'week': 3,
                        'title': 'Algorithms Mastery',
                        'tasks': [
                            'Dynamic Programming (1D, 2D, Matrix)',
                            'Greedy algorithms',
                            'Divide and Conquer',
                            'Solve 50+ medium-hard problems'
                        ],
                        'hours_per_day': 5
                    },
                    {
                        'week': 4,
                        'title': 'System Design & Architecture',
                        'tasks': [
                            'Low-level design (OOD, Design Patterns)',
                            'High-level design (Scalability, Load Balancing)',
                            'Database design and optimization',
                            'API design and microservices'
                        ],
                        'hours_per_day': 4
                    },
                    {
                        'week': 5,
                        'title': 'Core CS Advanced Topics',
                        'tasks': [
                            'Operating Systems (Concurrency, Deadlocks)',
                            'Distributed Systems concepts',
                            'Compiler design basics',
                            'Advanced networking protocols'
                        ],
                        'hours_per_day': 4
                    },
                    {
                        'week': 6,
                        'title': 'Company-Specific Preparation',
                        'tasks': [
                            'Solve company-specific questions',
                            'Study recent interview experiences',
                            'Practice behavioral questions (STAR method)',
                            'Prepare for leadership principles'
                        ],
                        'hours_per_day': 5
                    },
                    {
                        'week': 7,
                        'title': 'Mock Interviews & Optimization',
                        'tasks': [
                            'Daily 2 mock interviews',
                            'Code optimization practice',
                            'Whiteboard coding practice',
                            'Peer review and feedback'
                        ],
                        'hours_per_day': 6
                    },
                    {
                        'week': 8,
                        'title': 'Final Preparation',
                        'tasks': [
                            'Revise all important concepts',
                            'Practice with timed tests',
                            'Mental preparation and stress management',
                            'Final mock interviews with seniors'
                        ],
                        'hours_per_day': 5
                    }
                ]
            }
        }
        
        strategy = strategies.get(company.difficulty_level, strategies['Medium'])
        
        return Response({
            'company': company.name,
            'difficulty': company.difficulty_level,
            'total_weeks': strategy['weeks'],
            'plan': strategy['plan']
        })

    @action(detail=True, methods=['get'])
    def resources(self, request, pk=None):
        """Get learning resources for a specific company"""
        company = self.get_object()
        
        # Company-specific resources
        resources = {
            'youtube': [
                {
                    'title': f'{company.name} Interview Experience & Tips',
                    'type': 'Interview Experience',
                    'url': 'https://www.youtube.com/results?search_query=' + company.name + '+interview+experience',
                    'duration': 'Various'
                },
                {
                    'title': 'Complete DSA Course for Interviews',
                    'type': 'Course',
                    'url': 'https://www.youtube.com/results?search_query=DSA+complete+course+interview',
                    'duration': '20+ hours'
                },
                {
                    'title': 'Aptitude Preparation Complete Guide',
                    'type': 'Tutorial',
                    'url': 'https://www.youtube.com/results?search_query=aptitude+preparation+complete+guide',
                    'duration': '10+ hours'
                },
                {
                    'title': 'System Design Interview Preparation',
                    'type': 'Advanced',
                    'url': 'https://www.youtube.com/results?search_query=system+design+interview+preparation',
                    'duration': '15+ hours'
                }
            ],
            'articles': [
                {
                    'title': f'How to Crack {company.name} Interview',
                    'type': 'Guide',
                    'url': 'https://www.geeksforgeeks.org/',
                    'read_time': '15 min'
                },
                {
                    'title': 'Top 50 Interview Questions',
                    'type': 'Questions',
                    'url': 'https://www.geeksforgeeks.org/top-10-algorithms-in-interview-questions/',
                    'read_time': '30 min'
                },
                {
                    'title': 'Interview Preparation Checklist',
                    'type': 'Checklist',
                    'url': 'https://www.interviewbit.com/',
                    'read_time': '10 min'
                }
            ],
            'courses': [
                {
                    'title': 'Data Structures & Algorithms Masterclass',
                    'type': 'Udemy',
                    'url': 'https://www.udemy.com/courses/search/?q=data+structures+algorithms',
                    'price': 'Paid'
                },
                {
                    'title': 'System Design Interview Course',
                    'type': 'Educative',
                    'url': 'https://www.educative.io/courses/grokking-the-system-design-interview',
                    'price': 'Subscription'
                },
                {
                    'title': 'Aptitude & Reasoning Practice',
                    'type': 'IndiaBix',
                    'url': 'https://www.indiabix.com/',
                    'price': 'Free'
                }
            ],
            'practice': [
                {
                    'title': 'LeetCode - Company Questions',
                    'type': 'Coding Platform',
                    'url': f'https://leetcode.com/company/{company.name.lower()}/',
                    'problems': '100+'
                },
                {
                    'title': 'GeeksforGeeks - Company Portal',
                    'type': 'Practice',
                    'url': f'https://www.geeksforgeeks.org/company/{company.name.lower()}/',
                    'problems': '200+'
                },
                {
                    'title': 'HackerRank Practice',
                    'type': 'Coding Platform',
                    'url': 'https://www.hackerrank.com/',
                    'problems': '500+'
                }
            ]
        }
        
        return Response(resources)

    @action(detail=True, methods=['get'])
    def tips(self, request, pk=None):
        """Get interview tips for a specific company"""
        company = self.get_object()
        
        tips = {
            'dos': [
                'Research the company thoroughly before the interview',
                'Practice coding daily (at least 2-3 problems)',
                'Revise core CS fundamentals regularly',
                'Prepare your projects explanation with real-world impact',
                'Practice speaking clearly and confidently',
                'Dress professionally for the interview',
                'Arrive 15 minutes early (or test tech setup for virtual)',
                'Ask thoughtful questions at the end of interview',
                'Send a thank-you email after the interview',
                'Maintain good body language and eye contact'
            ],
            'donts': [
                'Don\'t fake knowledge - be honest about what you don\'t know',
                'Don\'t ignore HR questions - they matter equally',
                'Don\'t cram the night before - rest well',
                'Don\'t be late - punctuality is crucial',
                'Don\'t use mobile phone during interview',
                'Don\'t speak negatively about previous employers',
                'Don\'t interrupt the interviewer',
                'Don\'t give one-word answers - elaborate properly',
                'Don\'t panic if you don\'t know an answer - think out loud',
                'Don\'t forget to showcase your enthusiasm for the role'
            ],
            'common_mistakes': [
                'Not researching the company culture and values',
                'Focusing only on coding and ignoring aptitude/HR',
                'Poor communication during problem-solving',
                'Not practicing with time constraints',
                'Memorizing solutions instead of understanding concepts',
                'Not preparing questions to ask the interviewer',
                'Ignoring soft skills and behavioral preparation',
                'Last-minute preparation instead of consistent practice',
                'Not reviewing basics before the interview',
                'Getting stuck on one problem and not managing time'
            ],
            'success_tips': [
                f'Start preparation at least 4-8 weeks before {company.name} interview',
                'Create a structured study plan and follow it daily',
                'Practice with peers for mock interviews',
                'Record yourself answering questions to improve communication',
                'Focus on problem-solving approach, not just the solution',
                'Learn from every interview experience (even rejections)',
                'Stay updated with latest technology trends',
                'Build projects that demonstrate your skills',
                'Network with people working at the company',
                'Believe in yourself - confidence matters!'
            ]
        }
        
        return Response(tips)


class CompanyQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for viewing CompanyQuestion instances.
    Provides additional filtering capabilities.
    """
    queryset = CompanyQuestion.objects.select_related('company').all()
    serializer_class = CompanyQuestionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter questions by company, type, or difficulty"""
        queryset = super().get_queryset()
        
        # Filter by company
        company_id = self.request.query_params.get('company_id', None)
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        
        # Filter by question type
        question_type = self.request.query_params.get('question_type', None)
        if question_type:
            queryset = queryset.filter(question_type=question_type)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset
