from django.core.management.base import BaseCommand
from companies.models import Company, CompanyInterviewPattern, CompanyQuestion


class Command(BaseCommand):
    help = 'Populate database with sample company data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating company data...')

        # Create sample companies
        companies_data = [
            {
                'name': 'TCS',
                'description': 'Tata Consultancy Services is an Indian multinational information technology services and consulting company.',
                'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/TCS_Logo.svg/1200px-TCS_Logo.svg.png',
                'website': 'https://www.tcs.com',
                'industry': 'IT Services & Consulting',
                'interview_patterns': [
                    {'round_name': 'Aptitude', 'description': 'Online aptitude test covering quantitative, logical, and verbal ability', 'duration': '90 minutes', 'order': 1},
                    {'round_name': 'Technical', 'description': 'Technical interview focusing on programming fundamentals, OOPs, DBMS, and problem-solving', 'duration': '45 minutes', 'order': 2},
                    {'round_name': 'HR', 'description': 'HR interview to assess communication skills, cultural fit, and career goals', 'duration': '30 minutes', 'order': 3},
                ],
                'questions': [
                    {
                        'question': 'Tell me about yourself and why do you want to join TCS?',
                        'question_type': 'HR',
                        'answer': 'Start with your background, education, key skills. Mention TCS\'s reputation, global presence, learning opportunities, and how it aligns with your career goals.',
                        'difficulty': 'Easy',
                        'tags': 'introduction, motivation'
                    },
                    {
                        'question': 'What is the difference between C and C++?',
                        'question_type': 'Technical',
                        'answer': 'C is procedural while C++ supports both procedural and object-oriented programming. C++ supports classes, inheritance, polymorphism, while C does not. C++ provides better memory management features.',
                        'difficulty': 'Medium',
                        'tags': 'programming, OOPs'
                    },
                    {
                        'question': 'Write a program to reverse a string without using built-in functions.',
                        'question_type': 'Coding',
                        'answer': '''def reverse_string(s):
    result = ""
    for i in range(len(s)-1, -1, -1):
        result += s[i]
    return result

# Alternative approach using two pointers
def reverse_string_optimized(s):
    chars = list(s)
    left, right = 0, len(s) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    return ''.join(chars)''',
                        'difficulty': 'Easy',
                        'tags': 'string, algorithms'
                    },
                    {
                        'question': 'If a train travels at 60 km/h and reaches 1 hour late, what should be its speed to reach on time if the distance is 300 km?',
                        'question_type': 'Aptitude',
                        'answer': 'Time taken at 60 km/h = 300/60 = 5 hours. Since it\'s 1 hour late, actual time should be 4 hours. Required speed = 300/4 = 75 km/h',
                        'difficulty': 'Medium',
                        'tags': 'time-speed-distance'
                    }
                ]
            },
            {
                'name': 'Infosys',
                'description': 'Infosys Limited is an Indian multinational information technology company that provides business consulting, information technology and outsourcing services.',
                'logo': 'https://upload.wikimedia.org/wikipedia/en/thumb/8/87/Infosys_logo.svg/1200px-Infosys_logo.svg.png',
                'website': 'https://www.infosys.com',
                'industry': 'IT Services & Consulting',
                'interview_patterns': [
                    {'round_name': 'Aptitude', 'description': 'Online test with quantitative, reasoning, and verbal ability sections', 'duration': '75 minutes', 'order': 1},
                    {'round_name': 'Coding', 'description': 'Pseudocode and coding round to test programming logic', 'duration': '30 minutes', 'order': 2},
                    {'round_name': 'Technical', 'description': 'Face-to-face technical interview on CS fundamentals and projects', 'duration': '60 minutes', 'order': 3},
                    {'round_name': 'HR', 'description': 'Final HR discussion for cultural fit and role alignment', 'duration': '30 minutes', 'order': 4},
                ],
                'questions': [
                    {
                        'question': 'Why should we hire you over other candidates?',
                        'question_type': 'HR',
                        'answer': 'Highlight your unique combination of technical skills, problem-solving abilities, adaptability, and passion for technology. Give specific examples of projects or achievements that demonstrate these qualities.',
                        'difficulty': 'Medium',
                        'tags': 'self-assessment, value proposition'
                    },
                    {
                        'question': 'Explain the concept of normalization in databases.',
                        'question_type': 'Technical',
                        'answer': 'Normalization is organizing data to minimize redundancy. Forms include 1NF (atomic values), 2NF (no partial dependency), 3NF (no transitive dependency), BCNF. Benefits: reduces data duplication, improves integrity.',
                        'difficulty': 'Medium',
                        'tags': 'database, normalization'
                    },
                    {
                        'question': 'Find the second largest element in an array.',
                        'question_type': 'Coding',
                        'answer': '''def find_second_largest(arr):
    if len(arr) < 2:
        return None
    
    first = second = float('-inf')
    for num in arr:
        if num > first:
            second = first
            first = num
        elif num > second and num != first:
            second = num
    
    return second if second != float('-inf') else None''',
                        'difficulty': 'Medium',
                        'tags': 'array, sorting'
                    }
                ]
            },
            {
                'name': 'Amazon',
                'description': 'Amazon.com, Inc. is an American multinational technology company focusing on e-commerce, cloud computing, online advertising, digital streaming, and artificial intelligence.',
                'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Amazon_logo.svg/2560px-Amazon_logo.svg.png',
                'website': 'https://www.amazon.com',
                'industry': 'Technology & E-commerce',
                'interview_patterns': [
                    {'round_name': 'Aptitude', 'description': 'Online assessment with coding questions and work style assessment', 'duration': '90 minutes', 'order': 1},
                    {'round_name': 'Technical', 'description': 'Phone screening with data structures and algorithms questions', 'duration': '60 minutes', 'order': 2},
                    {'round_name': 'Technical', 'description': 'Virtual onsite with multiple technical rounds (DSA, System Design)', 'duration': '4-5 hours', 'order': 3},
                    {'round_name': 'Managerial', 'description': 'Bar Raiser and Hiring Manager rounds focusing on Leadership Principles', 'duration': '60 minutes', 'order': 4},
                ],
                'questions': [
                    {
                        'question': 'Tell me about a time when you went above and beyond for a customer.',
                        'question_type': 'Behavioral',
                        'answer': 'Use STAR method: Situation - describe the context, Task - your responsibility, Action - specific steps you took, Result - outcome and learnings. Focus on Customer Obsession leadership principle.',
                        'difficulty': 'Medium',
                        'tags': 'leadership principles, customer focus'
                    },
                    {
                        'question': 'Implement a function to check if a binary tree is a valid BST.',
                        'question_type': 'Coding',
                        'answer': '''class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isValidBST(root):
    def validate(node, low, high):
        if not node:
            return True
        if node.val <= low or node.val >= high:
            return False
        return (validate(node.left, low, node.val) and 
                validate(node.right, node.val, high))
    
    return validate(root, float(\'-inf\'), float(\'inf\'))''',
                        'difficulty': 'Hard',
                        'tags': 'binary tree, BST, recursion'
                    },
                    {
                        'question': 'Design a URL shortening service like bit.ly.',
                        'question_type': 'Technical',
                        'answer': 'Discuss: 1) Requirements (functional/non-functional), 2) API design, 3) Data model, 4) Algorithm (hash-based, base62 encoding), 5) Scalability (load balancer, cache, DB sharding), 6) Analytics tracking.',
                        'difficulty': 'Hard',
                        'tags': 'system design, scalability'
                    }
                ]
            },
            {
                'name': 'Wipro',
                'description': 'Wipro Limited is an Indian multinational corporation that provides information technology, consulting and business process services.',
                'logo': 'https://upload.wikimedia.org/wikipedia/en/thumb/0/0d/Wipro_Logo.svg/1200px-Wipro_Logo.svg.png',
                'website': 'https://www.wipro.com',
                'industry': 'IT Services & Consulting',
                'interview_patterns': [
                    {'round_name': 'Aptitude', 'description': 'Written test covering aptitude, reasoning, and verbal ability', 'duration': '60 minutes', 'order': 1},
                    {'round_name': 'Technical', 'description': 'Technical interview on programming, OS, DBMS, and networking concepts', 'duration': '45 minutes', 'order': 2},
                    {'round_name': 'HR', 'description': 'HR discussion for role fitment and expectations alignment', 'duration': '30 minutes', 'order': 3},
                ],
                'questions': [
                    {
                        'question': 'What are your strengths and weaknesses?',
                        'question_type': 'HR',
                        'answer': 'Be honest about strengths with examples. For weaknesses, mention genuine areas but show how you\'re working to improve them. Avoid clichés like "I\'m a perfectionist".',
                        'difficulty': 'Easy',
                        'tags': 'self-awareness, honesty'
                    },
                    {
                        'question': 'Explain the difference between TCP and UDP.',
                        'question_type': 'Technical',
                        'answer': 'TCP is connection-oriented, reliable, ensures delivery through acknowledgments, slower. UDP is connectionless, unreliable, no delivery guarantee, faster. TCP used for web/email, UDP for streaming/gaming.',
                        'difficulty': 'Medium',
                        'tags': 'networking, protocols'
                    }
                ]
            }
        ]

        # Create companies and related data
        for company_data in companies_data:
            company, created = Company.objects.get_or_create(
                name=company_data['name'],
                defaults={
                    'description': company_data['description'],
                    'logo': company_data.get('logo'),
                    'website': company_data.get('website'),
                    'industry': company_data.get('industry'),
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created company: {company.name}'))
            else:
                self.stdout.write(f'Company already exists: {company.name}')
            
            # Create interview patterns
            for pattern_data in company_data.get('interview_patterns', []):
                CompanyInterviewPattern.objects.create(
                    company=company,
                    **pattern_data
                )
            
            # Create questions
            for question_data in company_data.get('questions', []):
                CompanyQuestion.objects.create(
                    company=company,
                    **question_data
                )
        
        self.stdout.write(self.style.SUCCESS('\nSuccessfully populated sample company data!'))
        self.stdout.write(self.style.WARNING('\nNote: You can add more companies by running this command again or adding data through Django admin.'))
