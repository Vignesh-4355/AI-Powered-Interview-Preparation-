"""Management command to populate mock interview questions"""
from django.core.management.base import BaseCommand
from mock_interview.models import InterviewQuestion


class Command(BaseCommand):
    help = 'Populate database with comprehensive mock interview questions'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating mock interview questions...')

        questions = [
            # HR Questions - Easy (5)
            {
                'question_text': 'Tell me about yourself.',
                'question_type': 'HR',
                'difficulty': 'Easy',
                'expected_keywords': ['education', 'experience', 'skills', 'background', 'career', 'goals'],
                'model_answer': 'Start with education, mention relevant experience, highlight key skills, and connect to career goals.',
            },
            {
                'question_text': 'Why do you want to work for our company?',
                'question_type': 'HR',
                'difficulty': 'Easy',
                'expected_keywords': ['research', 'values', 'culture', 'growth', 'alignment', 'mission', 'reputation'],
                'model_answer': 'Show you researched the company, mention alignment with values, growth opportunities, and company reputation.',
            },
            {
                'question_text': 'What are your strengths?',
                'question_type': 'HR',
                'difficulty': 'Easy',
                'expected_keywords': ['technical', 'communication', 'leadership', 'problem-solving', 'teamwork', 'adaptability'],
                'model_answer': 'Mention 2-3 relevant strengths with examples. Include both technical and soft skills.',
            },
            {
                'question_text': 'What are your weaknesses?',
                'question_type': 'HR',
                'difficulty': 'Easy',
                'expected_keywords': ['improvement', 'learning', 'honest', 'working', 'overcome', 'development'],
                'model_answer': 'Be honest but show how you are working to improve. Mention specific steps taken.',
            },
            {
                'question_text': 'Where do you see yourself in 5 years?',
                'question_type': 'HR',
                'difficulty': 'Easy',
                'expected_keywords': ['growth', 'leadership', 'expertise', 'contribution', 'career', 'development', 'goals'],
                'model_answer': 'Show ambition but remain realistic. Mention growth in expertise, leadership, and contribution to company.',
            },

            # HR Questions - Medium (5)
            {
                'question_text': 'Describe a challenging situation at work and how you handled it.',
                'question_type': 'HR',
                'difficulty': 'Medium',
                'expected_keywords': ['problem', 'solution', 'communication', 'teamwork', 'result', 'learning', 'approach'],
                'model_answer': 'Use STAR method: Situation, Task, Action, Result. Focus on your approach and what you learned.',
            },
            {
                'question_text': 'How do you handle pressure and stressful situations?',
                'question_type': 'HR',
                'difficulty': 'Medium',
                'expected_keywords': ['prioritize', 'organized', 'calm', 'time-management', 'break', 'communicate', 'focus'],
                'model_answer': 'Explain your stress management techniques: prioritization, staying organized, taking breaks, communicating with team.',
            },
            {
                'question_text': 'Why should we hire you?',
                'question_type': 'HR',
                'difficulty': 'Medium',
                'expected_keywords': ['skills', 'experience', 'value', 'unique', 'contribution', 'fit', 'achievements'],
                'model_answer': 'Highlight unique skills, relevant experience, specific achievements, and cultural fit. Show value you bring.',
            },
            {
                'question_text': 'Describe a time when you showed leadership.',
                'question_type': 'HR',
                'difficulty': 'Medium',
                'expected_keywords': ['initiative', 'team', 'guidance', 'result', 'motivation', 'decision', 'responsibility'],
                'model_answer': 'Use STAR method. Show how you took initiative, guided team, made decisions, and achieved results.',
            },
            {
                'question_text': 'How do you handle conflicts in a team?',
                'question_type': 'HR',
                'difficulty': 'Medium',
                'expected_keywords': ['communication', 'listen', 'understand', 'compromise', 'respect', 'solution', 'mediation'],
                'model_answer': 'Emphasize active listening, understanding different perspectives, finding common ground, and respectful communication.',
            },

            # HR Questions - Hard (3)
            {
                'question_text': 'Tell me about a time you failed and what you learned from it.',
                'question_type': 'HR',
                'difficulty': 'Hard',
                'expected_keywords': ['accountability', 'lesson', 'improvement', 'reflection', 'growth', 'mistake', 'resilience'],
                'model_answer': 'Show accountability, explain what you learned, how you improved, and how it made you stronger.',
            },
            {
                'question_text': 'How would you handle a disagreement with your manager?',
                'question_type': 'HR',
                'difficulty': 'Hard',
                'expected_keywords': ['respect', 'data', 'discussion', 'perspective', 'professional', 'compromise', 'understanding'],
                'model_answer': 'Show professional approach: present data, have respectful discussion, understand their perspective, find compromise.',
            },
            {
                'question_text': 'What would you do if you noticed a colleague violating company policy?',
                'question_type': 'HR',
                'difficulty': 'Hard',
                'expected_keywords': ['report', 'ethics', 'policy', 'professional', 'HR', 'integrity', 'responsibility'],
                'model_answer': 'Show ethical responsibility: document situation, report to appropriate authority (HR/manager), maintain professionalism.',
            },

            # Technical Questions - Easy (5)
            {
                'question_text': 'What is the difference between a class and an object in OOP?',
                'question_type': 'Technical',
                'difficulty': 'Easy',
                'expected_keywords': ['blueprint', 'instance', 'properties', 'methods', 'inheritance', 'template', 'creation'],
                'model_answer': 'A class is a blueprint/template that defines properties and methods. An object is an instance of a class created from that blueprint.',
            },
            {
                'question_text': 'Explain what an API is.',
                'question_type': 'Technical',
                'difficulty': 'Easy',
                'expected_keywords': ['interface', 'communication', 'request', 'response', 'protocol', 'integration', 'services'],
                'model_answer': 'API (Application Programming Interface) is a set of protocols that allows different software applications to communicate with each other through requests and responses.',
            },
            {
                'question_text': 'What is version control and why is it important?',
                'question_type': 'Technical',
                'difficulty': 'Easy',
                'expected_keywords': ['tracking', 'changes', 'collaboration', 'history', 'git', 'branches', 'revert'],
                'model_answer': 'Version control tracks changes in code over time, enables collaboration, maintains history, allows branching, and helps revert to previous versions.',
            },
            {
                'question_text': 'What is the difference between SQL and NoSQL databases?',
                'question_type': 'Technical',
                'difficulty': 'Easy',
                'expected_keywords': ['relational', 'schema', 'tables', 'documents', 'scalability', 'structure', 'flexibility'],
                'model_answer': 'SQL databases are relational with structured tables and fixed schemas. NoSQL databases are flexible, storing documents, key-values, or graphs without fixed schemas.',
            },
            {
                'question_text': 'Explain what a REST API is.',
                'question_type': 'Technical',
                'difficulty': 'Easy',
                'expected_keywords': ['HTTP', 'methods', 'stateless', 'resources', 'endpoints', 'JSON', 'CRUD'],
                'model_answer': 'REST API uses HTTP methods (GET, POST, PUT, DELETE) to manipulate resources. It is stateless, uses endpoints, and typically exchanges JSON data for CRUD operations.',
            },

            # Technical Questions - Medium (5)
            {
                'question_text': 'What is the difference between authentication and authorization?',
                'question_type': 'Technical',
                'difficulty': 'Medium',
                'expected_keywords': ['identity', 'verification', 'permissions', 'access', 'login', 'roles', 'security'],
                'model_answer': 'Authentication verifies who you are (identity/login). Authorization determines what you have permission to access (roles/permissions).',
            },
            {
                'question_text': 'Explain the concept of microservices architecture.',
                'question_type': 'Technical',
                'difficulty': 'Medium',
                'expected_keywords': ['services', 'independent', 'deployment', 'scalability', 'communication', 'modular', 'APIs'],
                'model_answer': 'Microservices breaks application into small, independent services that communicate via APIs. Each service handles specific functionality, enabling independent deployment and scalability.',
            },
            {
                'question_text': 'What is CI/CD and why is it important?',
                'question_type': 'Technical',
                'difficulty': 'Medium',
                'expected_keywords': ['continuous', 'integration', 'deployment', 'automation', 'testing', 'pipeline', 'delivery'],
                'model_answer': 'CI/CD (Continuous Integration/Continuous Deployment) automates code integration, testing, and deployment. It ensures faster, reliable releases with automated testing pipelines.',
            },
            {
                'question_text': 'How does caching improve application performance?',
                'question_type': 'Technical',
                'difficulty': 'Medium',
                'expected_keywords': ['memory', 'faster', 'retrieval', 'storage', 'latency', 'redis', 'optimization'],
                'model_answer': 'Caching stores frequently accessed data in memory for faster retrieval, reducing database queries, decreasing latency, and improving overall application performance.',
            },
            {
                'question_text': 'What is the difference between synchronous and asynchronous programming?',
                'question_type': 'Technical',
                'difficulty': 'Medium',
                'expected_keywords': ['blocking', 'non-blocking', 'concurrent', 'callback', 'promise', 'parallel', 'execution'],
                'model_answer': 'Synchronous executes code sequentially (blocking). Asynchronous allows non-blocking execution, enabling concurrent operations using callbacks, promises, or async/await.',
            },

            # Technical Questions - Hard (3)
            {
                'question_text': 'Explain the concept of database indexing and its trade-offs.',
                'question_type': 'Technical',
                'difficulty': 'Hard',
                'expected_keywords': ['performance', 'query', 'B-tree', 'write', 'storage', 'optimization', 'lookup'],
                'model_answer': 'Indexes improve query performance using data structures like B-trees for faster lookups. Trade-offs: increased storage space, slower write operations, maintenance overhead.',
            },
            {
                'question_text': 'What are design patterns? Explain Singleton and Factory patterns.',
                'question_type': 'Technical',
                'difficulty': 'Hard',
                'expected_keywords': ['reusable', 'solution', 'instance', 'creation', 'interface', 'object', 'best-practice'],
                'model_answer': 'Design patterns are reusable solutions to common problems. Singleton ensures single instance. Factory creates objects without specifying exact class, providing flexible object creation.',
            },
            {
                'question_text': 'How would you design a URL shortening service like bit.ly?',
                'question_type': 'Technical',
                'difficulty': 'Hard',
                'expected_keywords': ['database', 'hash', 'redirect', 'scalability', 'caching', 'unique', 'analytics'],
                'model_answer': 'Use hashing algorithm to generate short codes, store mappings in database, implement 301 redirects, add caching for performance, track analytics, ensure uniqueness and scalability.',
            },

            # Coding Questions - Easy (3)
            {
                'question_text': 'How would you reverse a string in Python?',
                'question_type': 'Coding',
                'difficulty': 'Easy',
                'expected_keywords': ['slice', 'reversed', 'iteration', 'join', 'syntax', '[::-1]', 'loop'],
                'model_answer': 'Use string slicing: string[::-1]. Or use reversed() function with join: "".join(reversed(string)). Or iterate backwards and build new string.',
            },
            {
                'question_text': 'Write a function to check if a number is prime.',
                'question_type': 'Coding',
                'difficulty': 'Easy',
                'expected_keywords': ['loop', 'divisible', 'range', 'optimization', 'sqrt', 'condition', 'return'],
                'model_answer': 'Check if number < 2 (not prime). Loop from 2 to sqrt(n). If divisible by any number, not prime. Otherwise, prime.',
            },
            {
                'question_text': 'How do you find the maximum element in an array?',
                'question_type': 'Coding',
                'difficulty': 'Easy',
                'expected_keywords': ['iterate', 'compare', 'max', 'loop', 'track', 'built-in', 'complexity'],
                'model_answer': 'Initialize max with first element. Iterate through array, compare each element with max, update if larger. Or use built-in max() function. Time complexity: O(n).',
            },

            # Coding Questions - Medium (3)
            {
                'question_text': 'Explain how you would implement a binary search algorithm.',
                'question_type': 'Coding',
                'difficulty': 'Medium',
                'expected_keywords': ['sorted', 'divide', 'conquer', 'mid', 'recursive', 'iterative', 'logarithmic'],
                'model_answer': 'Works on sorted arrays. Compare target with middle element. If equal, return index. If smaller, search left half. If larger, search right half. Repeat. O(log n) time complexity.',
            },
            {
                'question_text': 'How would you detect a cycle in a linked list?',
                'question_type': 'Coding',
                'difficulty': 'Medium',
                'expected_keywords': ['pointer', 'slow', 'fast', 'Floyd', 'cycle', 'meeting', 'detection'],
                'model_answer': "Use Floyd's Cycle Detection: two pointers (slow moves 1 step, fast moves 2 steps). If they meet, cycle exists. If fast reaches end, no cycle. O(n) time, O(1) space.",
            },
            {
                'question_text': 'Explain how to implement a stack using arrays.',
                'question_type': 'Coding',
                'difficulty': 'Medium',
                'expected_keywords': ['LIFO', 'push', 'pop', 'top', 'array', 'index', 'overflow'],
                'model_answer': 'Use array with top index. Push: increment top, add element. Pop: return element at top, decrement top. Check overflow/underflow. LIFO principle. O(1) operations.',
            },

            # Coding Questions - Hard (2)
            {
                'question_text': 'How would you optimize a slow database query?',
                'question_type': 'Coding',
                'difficulty': 'Hard',
                'expected_keywords': ['index', 'explain', 'normalize', 'cache', 'join', 'select', 'analyze'],
                'model_answer': 'Use EXPLAIN to analyze query. Add indexes on frequently queried columns. Optimize JOINs. Avoid SELECT *. Consider denormalization. Use caching. Partition large tables.',
            },
            {
                'question_text': 'Design a rate limiting system for an API.',
                'question_type': 'Coding',
                'difficulty': 'Hard',
                'expected_keywords': ['token', 'bucket', 'sliding', 'window', 'redis', 'counter', 'throttle'],
                'model_answer': 'Use token bucket or sliding window algorithm. Store counters in Redis for speed. Track requests per user/IP. Return 429 status when limit exceeded. Implement distributed rate limiting.',
            },
        ]

        # Create questions
        created_count = 0
        for q_data in questions:
            question, created = InterviewQuestion.objects.get_or_create(
                question_text=q_data['question_text'],
                defaults=q_data
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'✓ Successfully created/verified {created_count} interview questions!'))
        self.stdout.write(self.style.SUCCESS(f'Total questions in database: {InterviewQuestion.objects.count()}'))
        
        # Show breakdown
        self.stdout.write('\nBreakdown by type:')
        for q_type in ['HR', 'Technical', 'Coding']:
            count = InterviewQuestion.objects.filter(question_type=q_type).count()
            self.stdout.write(f'  {q_type}: {count} questions')
        
        self.stdout.write('\nBreakdown by difficulty:')
        for diff in ['Easy', 'Medium', 'Hard']:
            count = InterviewQuestion.objects.filter(difficulty=diff).count()
            self.stdout.write(f'  {diff}: {count} questions')
