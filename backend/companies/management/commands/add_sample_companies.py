from django.core.management.base import BaseCommand
from companies.models import Company, CompanyInterviewPattern, CompanyQuestion


class Command(BaseCommand):
    help = 'Add sample company data for interview preparation'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding sample company data...')

        # Company 1: TCS
        tcs, created = Company.objects.get_or_create(
            name='Tata Consultancy Services (TCS)',
            defaults={
                'description': 'India\'s largest IT services company known for its rigorous aptitude tests and technical interviews.',
                'logo': 'https://logo.clearbit.com/tcs.com',
                'website': 'https://www.tcs.com',
                'industry': 'IT Services & Consulting',
                'difficulty_level': 'Easy',
                'hiring_frequency': 'High',
                'total_questions': 150,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {tcs.name}'))

        # Company 2: Infosys
        infosys, created = Company.objects.get_or_create(
            name='Infosys',
            defaults={
                'description': 'Global leader in next-generation digital services and consulting with structured interview process.',
                'logo': 'https://logo.clearbit.com/infosys.com',
                'website': 'https://www.infosys.com',
                'industry': 'IT Services & Consulting',
                'difficulty_level': 'Easy',
                'hiring_frequency': 'High',
                'total_questions': 140,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {infosys.name}'))

        # Company 3: Amazon
        amazon, created = Company.objects.get_or_create(
            name='Amazon',
            defaults={
                'description': 'World\'s largest e-commerce and cloud company known for challenging technical interviews and leadership principles.',
                'logo': 'https://logo.clearbit.com/amazon.com',
                'website': 'https://www.amazon.com',
                'industry': 'E-commerce & Cloud Computing',
                'difficulty_level': 'Hard',
                'hiring_frequency': 'Medium',
                'total_questions': 200,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {amazon.name}'))

        # Company 4: Wipro
        wipro, created = Company.objects.get_or_create(
            name='Wipro',
            defaults={
                'description': 'Leading global information technology, consulting and business process services company.',
                'logo': 'https://logo.clearbit.com/wipro.com',
                'website': 'https://www.wipro.com',
                'industry': 'IT Services & Consulting',
                'difficulty_level': 'Medium',
                'hiring_frequency': 'Medium',
                'total_questions': 120,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created: {wipro.name}'))

        # Add interview patterns for TCS
        if created or tcs.interview_patterns.count() == 0:
            patterns_data = [
                ('Aptitude', 'Online aptitude test covering quantitative, logical reasoning, and verbal ability', '60 minutes', 1),
                ('Technical', 'Technical interview focusing on programming, DSA, and core CS concepts', '45 minutes', 2),
                ('HR', 'HR interview assessing communication, attitude, and cultural fit', '30 minutes', 3),
            ]
            for round_name, desc, duration, order in patterns_data:
                CompanyInterviewPattern.objects.get_or_create(
                    company=tcs,
                    round_name=round_name,
                    defaults={
                        'description': desc,
                        'duration': duration,
                        'order': order,
                    }
                )

        # Add sample questions for TCS
        if created or tcs.questions.count() == 0:
            questions_data = [
                (
                    'Tell me about yourself and why do you want to join TCS?',
                    'HR',
                    'Easy',
                    'Start with a brief introduction about your educational background, skills, and projects. Then mention why TCS appeals to you - its reputation, training programs, growth opportunities, and how it aligns with your career goals.',
                ),
                (
                    'Explain the difference between C++ and Java.',
                    'Technical',
                    'Medium',
                    'C++ supports multiple inheritance and pointers, while Java doesn\'t. Java has automatic garbage collection, is platform-independent (runs on JVM), and has built-in multithreading support. C++ is faster and gives more control over system resources.',
                ),
            ]
            for question, qtype, difficulty, answer in questions_data:
                CompanyQuestion.objects.get_or_create(
                    company=tcs,
                    question=question,
                    defaults={
                        'question_type': qtype,
                        'answer': answer,
                        'difficulty': difficulty,
                    }
                )

        self.stdout.write(self.style.SUCCESS('\n✅ Sample company data added successfully!'))
        self.stdout.write(f'\nTotal companies: {Company.objects.count()}')
