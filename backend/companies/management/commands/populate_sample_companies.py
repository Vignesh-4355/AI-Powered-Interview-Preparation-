"""Management command to populate sample company data"""
from django.core.management.base import BaseCommand
from companies.models import Company, CompanyInterviewPattern


class Command(BaseCommand):
    help = 'Populate database with sample companies'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample companies...')

        # Sample companies data
        companies_data = [
            {
                'name': 'TCS',
                'description': 'Tata Consultancy Services - Leading IT services, business solutions and outsourcing company',
                'logo': 'https://logo.clearbit.com/tcs.com',
                'website': 'https://www.tcs.com',
                'industry': 'IT Services & Consulting',
                'difficulty_level': 'Easy',
                'hiring_frequency': 'High',
                'total_questions': 250,
            },
            {
                'name': 'Infosys',
                'description': 'Global leader in next-generation digital services and consulting',
                'logo': 'https://logo.clearbit.com/infosys.com',
                'website': 'https://www.infosys.com',
                'industry': 'IT Services & Consulting',
                'difficulty_level': 'Easy',
                'hiring_frequency': 'High',
                'total_questions': 230,
            },
            {
                'name': 'Amazon',
                'description': 'Multinational technology company focusing on e-commerce, cloud computing, and AI',
                'logo': 'https://logo.clearbit.com/amazon.com',
                'website': 'https://www.amazon.com',
                'industry': 'Technology & E-commerce',
                'difficulty_level': 'Hard',
                'hiring_frequency': 'Medium',
                'total_questions': 450,
            },
            {
                'name': 'Wipro',
                'description': 'Leading global information technology, consulting and business process services company',
                'logo': 'https://logo.clearbit.com/wipro.com',
                'website': 'https://www.wipro.com',
                'industry': 'IT Services & Consulting',
                'difficulty_level': 'Easy',
                'hiring_frequency': 'High',
                'total_questions': 200,
            },
            {
                'name': 'Microsoft',
                'description': 'Technology corporation developing computer software, consumer electronics, and personal computers',
                'logo': 'https://logo.clearbit.com/microsoft.com',
                'website': 'https://www.microsoft.com',
                'industry': 'Technology & Software',
                'difficulty_level': 'Hard',
                'hiring_frequency': 'Medium',
                'total_questions': 500,
            },
            {
                'name': 'Google',
                'description': 'Multinational technology company specializing in Internet-related services and products',
                'logo': 'https://logo.clearbit.com/google.com',
                'website': 'https://www.google.com',
                'industry': 'Technology & Internet',
                'difficulty_level': 'Hard',
                'hiring_frequency': 'Low',
                'total_questions': 600,
            },
            {
                'name': 'Accenture',
                'description': 'Global professional services company providing strategy, consulting, digital, technology and operations services',
                'logo': 'https://logo.clearbit.com/accenture.com',
                'website': 'https://www.accenture.com',
                'industry': 'Consulting & Technology',
                'difficulty_level': 'Medium',
                'hiring_frequency': 'High',
                'total_questions': 300,
            },
            {
                'name': 'Cognizant',
                'description': 'Multinational information technology services and consulting company',
                'logo': 'https://logo.clearbit.com/cognizant.com',
                'website': 'https://www.cognizant.com',
                'industry': 'IT Services & Consulting',
                'difficulty_level': 'Easy',
                'hiring_frequency': 'High',
                'total_questions': 220,
            },
            {
                'name': 'Deloitte',
                'description': 'Multinational professional services network providing audit, consulting, financial advisory, and tax services',
                'logo': 'https://logo.clearbit.com/deloitte.com',
                'website': 'https://www.deloitte.com',
                'industry': 'Consulting & Advisory',
                'difficulty_level': 'Medium',
                'hiring_frequency': 'Medium',
                'total_questions': 280,
            },
            {
                'name': 'IBM',
                'description': 'Multinational technology corporation producing and selling computer hardware, middleware and software',
                'logo': 'https://logo.clearbit.com/ibm.com',
                'website': 'https://www.ibm.com',
                'industry': 'Technology & Consulting',
                'difficulty_level': 'Medium',
                'hiring_frequency': 'Medium',
                'total_questions': 350,
            },
        ]

        created_count = 0
        for company_data in companies_data:
            company, created = Company.objects.get_or_create(
                name=company_data['name'],
                defaults=company_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created company: {company.name}'))
                created_count += 1
                
                # Add interview patterns
                patterns = [
                    {
                        'round_name': 'Aptitude',
                        'description': 'Aptitude test covering quantitative, logical reasoning, and verbal ability',
                        'duration': '60 minutes',
                        'order': 1,
                    },
                    {
                        'round_name': 'Coding',
                        'description': 'Coding round to assess programming skills and problem-solving abilities',
                        'duration': '90 minutes',
                        'order': 2,
                    },
                    {
                        'round_name': 'Technical',
                        'description': 'Technical interview covering core CS concepts, projects, and domain knowledge',
                        'duration': '45-60 minutes',
                        'order': 3,
                    },
                    {
                        'round_name': 'HR',
                        'description': 'HR interview assessing cultural fit, communication skills, and career goals',
                        'duration': '30-45 minutes',
                        'order': 4,
                    },
                ]
                
                for pattern_data in patterns:
                    CompanyInterviewPattern.objects.get_or_create(
                        company=company,
                        round_name=pattern_data['round_name'],
                        defaults=pattern_data
                    )
            else:
                self.stdout.write(self.style.WARNING(f'⊘ Company already exists: {company.name}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully created {created_count} companies!'))
        self.stdout.write(self.style.SUCCESS('✓ Interview patterns added for new companies'))
