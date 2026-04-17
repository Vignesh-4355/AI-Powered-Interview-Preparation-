from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Q
from .models import RoadmapItem
from .serializers import RoadmapItemSerializer
from coding_practice.models import CodingQuestion, UserProgress
from aptitude.models import AptitudeQuestion, UserAttempt
from hrgd.models import HRQuestion
from companies.models import Company


class RoadmapViewSet(viewsets.ModelViewSet):
    """
    ViewSet for personalized roadmap.
    
    Logic:
    - Analyze user attempts in coding, aptitude, HR
    - Identify weak areas (low accuracy, few attempts)
    - Consider preferred company
    - Generate dynamic personalized roadmap
    """
    serializer_class = RoadmapItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RoadmapItem.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def generate(self, request):
        """Generate or regenerate personalized roadmap"""
        # Delete old incomplete roadmap items
        RoadmapItem.objects.filter(
            user=request.user,
            status__in=['Not Started', 'In Progress']
        ).delete()
        
        # Analyze user performance
        coding_stats = self._analyze_coding_performance(request.user)
        aptitude_stats = self._analyze_aptitude_performance(request.user)
        hr_stats = self._analyze_hr_performance(request.user)
        company_preference = self._get_company_preference(request.user)
        
        # Generate roadmap items
        roadmap_items = []
        
        # Coding recommendations based on performance
        roadmap_items.extend(self._generate_coding_tasks(
            request.user, coding_stats, company_preference
        ))
        
        # Aptitude recommendations
        roadmap_items.extend(self._generate_aptitude_tasks(
            request.user, aptitude_stats
        ))
        
        # HR preparation
        roadmap_items.extend(self._generate_hr_tasks(
            request.user, hr_stats, company_preference
        ))
        
        # Mock interview recommendation
        roadmap_items.append(self._create_mock_interview_task(request.user))
        
        # Sort by priority
        priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        roadmap_items.sort(key=lambda x: priority_order.get(x.priority, 2))
        
        # Set order and save
        for idx, item in enumerate(roadmap_items):
            item.order = idx
            item.save()
        
        serializer = self.get_serializer(roadmap_items, many=True)
        return Response(serializer.data)

    def _analyze_coding_performance(self, user):
        """Analyze coding practice performance"""
        solved_count = UserProgress.objects.filter(
            user=user, is_solved=True
        ).count()
        
        # Get topics attempted
        topic_attempts = UserProgress.objects.filter(
            user=user
        ).values('question__topic').annotate(
            total=Count('id'),
            solved=Count('id', filter=Q(is_solved=True))
        )
        
        weak_topics = []
        for topic_stat in topic_attempts:
            accuracy = (topic_stat['solved'] / topic_stat['total'] * 100) if topic_stat['total'] > 0 else 0
            if accuracy < 50 or topic_stat['total'] < 3:
                weak_topics.append({
                    'topic': topic_stat['question__topic'],
                    'accuracy': accuracy,
                    'attempts': topic_stat['total']
                })
        
        return {
            'solved_count': solved_count,
            'weak_topics': weak_topics
        }

    def _analyze_aptitude_performance(self, user):
        """Analyze aptitude performance"""
        attempts = UserAttempt.objects.filter(user=user)
        total = attempts.count()
        correct = attempts.filter(is_correct=True).count()
        accuracy = (correct / total * 100) if total > 0 else 0
        
        # By category
        category_stats = {}
        for category in ['Time and Work', 'Time and Distance', 'Probability', 'Percentages', 'Logical Reasoning']:
            cat_attempts = attempts.filter(question__category=category)
            cat_correct = cat_attempts.filter(is_correct=True).count()
            cat_accuracy = (cat_correct / cat_attempts.count() * 100) if cat_attempts.count() > 0 else 0
            category_stats[category] = {
                'accuracy': cat_accuracy,
                'attempts': cat_attempts.count()
            }
        
        return {
            'total_attempts': total,
            'accuracy': accuracy,
            'category_stats': category_stats
        }

    def _analyze_hr_performance(self, user):
        """Analyze HR preparation"""
        hr_count = HRQuestion.objects.count()
        return {
            'prepared': hr_count > 0,
        }

    def _get_company_preference(self, user):
        """Get user's preferred company"""
        return None

    def _generate_coding_tasks(self, user, stats, company):
        """Generate coding practice tasks"""
        tasks = []
        
        if stats['solved_count'] < 10:
            tasks.append(RoadmapItem(
                user=user,
                topic='Data Structures Fundamentals',
                description='Master arrays, strings, linked lists, stacks, and queues. Practice 5-10 problems on each topic.',
                priority='Critical',
                category='Data Structures',
                estimated_hours=15
            ))
        else:
            for weak_topic in stats['weak_topics'][:3]:
                tasks.append(RoadmapItem(
                    user=user,
                    topic=f"Improve {weak_topic['topic']}",
                    description=f'Focus on {weak_topic["topic"]} problems. Current accuracy: {weak_topic["accuracy"]:.1f}%. Solve 5-7 more problems.',
                    priority='High' if weak_topic['accuracy'] < 30 else 'Medium',
                    category='Coding Practice',
                    estimated_hours=8
                ))
        
        return tasks

    def _generate_aptitude_tasks(self, user, stats):
        """Generate aptitude tasks"""
        tasks = []
        
        if stats['total_attempts'] < 20:
            tasks.append(RoadmapItem(
                user=user,
                topic='Aptitude Fundamentals',
                description='Practice basic aptitude questions across all categories. Aim for 50+ total attempts.',
                priority='High',
                category='Aptitude',
                estimated_hours=10
            ))
        
        for category, cat_stats in stats['category_stats'].items():
            if cat_stats['accuracy'] < 60 or cat_stats['attempts'] < 5:
                tasks.append(RoadmapItem(
                    user=user,
                    topic=f'{category} Practice',
                    description=f'Improve {category} skills. Current accuracy: {cat_stats["accuracy"]:.1f}%. Practice 10+ questions.',
                    priority='Medium',
                    category='Aptitude',
                    estimated_hours=6
                ))
        
        return tasks

    def _generate_hr_tasks(self, user, stats, company):
        """Generate HR preparation tasks"""
        tasks = []
        
        if not stats['prepared']:
            tasks.append(RoadmapItem(
                user=user,
                topic='HR Interview Preparation',
                description='Practice common HR questions: Tell me about yourself, strengths/weaknesses, behavioral questions using STAR method.',
                priority='High',
                category='HR Preparation',
                estimated_hours=8
            ))
        
        if company:
            tasks.append(RoadmapItem(
                user=user,
                topic=f'{company.name} Research',
                description=f'Research {company.name}: company culture, recent news, products, values, and interview pattern.',
                priority='High',
                category='Company Research',
                estimated_hours=4
            ))
        
        return tasks

    def _create_mock_interview_task(self, user):
        """Create mock interview task"""
        return RoadmapItem(
            user=user,
            topic='Mock Interview Challenge',
            description='Take at least 3 full-length mock interviews to simulate real interview experience and track improvement.',
            priority='Critical',
            category='Mock Interviews',
            estimated_hours=3
        )

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark a roadmap item as completed"""
        item = self.get_object()
        item.status = 'Completed'
        item.completed_at = timezone.now()
        item.save()
        
        return Response({
            'message': 'Roadmap item marked as completed!',
            'completed_at': item.completed_at.isoformat()
        })

    @action(detail=True, methods=['post'])
    def mark_in_progress(self, request, pk=None):
        """Mark a roadmap item as in progress"""
        item = self.get_object()
        item.status = 'In Progress'
        item.save()
        
        return Response({
            'message': 'Roadmap item marked as in progress!'
        })

    @action(detail=False, methods=['get'])
    def progress(self, request):
        """Get overall roadmap progress"""
        queryset = self.get_queryset()
        total = queryset.count()
        completed = queryset.filter(status='Completed').count()
        in_progress = queryset.filter(status='In Progress').count()
        not_started = queryset.filter(status='Not Started').count()
        
        completion_percentage = (completed / total * 100) if total > 0 else 0
        
        category_progress = {}
        for category in dict(RoadmapItem.CATEGORY_CHOICES).keys():
            cat_total = queryset.filter(category=category).count()
            cat_completed = queryset.filter(category=category, status='Completed').count()
            category_progress[category] = {
                'total': cat_total,
                'completed': cat_completed,
                'percentage': (cat_completed / cat_total * 100) if cat_total > 0 else 0
            }
        
        return Response({
            'total_items': total,
            'completed': completed,
            'in_progress': in_progress,
            'not_started': not_started,
            'completion_percentage': round(completion_percentage, 2),
            'by_category': category_progress
        })
