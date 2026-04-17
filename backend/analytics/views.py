from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Avg, Q, F
from datetime import datetime, timedelta
from .models import UserProgress
from .serializers import UserProgressSerializer, DetailedAnalyticsSerializer
from coding_practice.models import UserProgress as CodingProgress
from aptitude.models import UserAttempt as AptitudeAttempt
from roadmap.models import RoadmapItem
from companies.models import Company


class AnalyticsView(views.APIView):
    """API endpoint for comprehensive user analytics"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get detailed analytics for the authenticated user"""
        user = request.user
        
        # Get or create user progress tracker
        progress, _ = UserProgress.objects.get_or_create(user=user)
        
        # Update progress stats from actual data
        self._update_progress_stats(progress)
        
        # Gather detailed statistics
        coding_stats = self._get_coding_stats(user)
        aptitude_stats = self._get_aptitude_stats(user)
        company_stats = self._get_company_stats(user)
        roadmap_stats = self._get_roadmap_stats(user)
        recent_activity = self._get_recent_activity(user)
        
        analytics_data = {
            'progress': UserProgressSerializer(progress).data,
            'coding_stats': coding_stats,
            'aptitude_stats': aptitude_stats,
            'mock_interview_stats': {'total_sessions': 0, 'completed_sessions': 0, 'average_score': 0},
            'company_prep_stats': company_stats,
            'roadmap_stats': roadmap_stats,
            'recent_activity': recent_activity,
        }
        
        return Response(analytics_data)

    def _update_progress_stats(self, progress):
        """Update progress tracker with latest data"""
        # Coding stats
        coding_attempts = CodingProgress.objects.filter(user=progress.user)
        progress.coding_attempted = coding_attempts.count()
        progress.coding_solved = coding_attempts.filter(is_solved=True).count()
        if coding_attempts.exists():
            progress.last_coding_activity = coding_attempts.latest('last_attempted_at').last_attempted_at
        
        # Aptitude stats
        aptitude_attempts = AptitudeAttempt.objects.filter(user=progress.user)
        progress.aptitude_attempted = aptitude_attempts.count()
        progress.aptitude_correct = aptitude_attempts.filter(is_correct=True).count()
        if aptitude_attempts.exists():
            progress.last_aptitude_activity = aptitude_attempts.latest('attempted_at').attempted_at
        
        progress.save()

    def _get_coding_stats(self, user):
        """Get detailed coding statistics"""
        attempts = CodingProgress.objects.filter(user=user)
        
        # By difficulty
        difficulty_breakdown = dict(
            attempts.values('question__difficulty')
            .annotate(count=Count('id'), solved=Count('id', filter=Q(is_solved=True)))
        )
        
        # By topic
        topic_breakdown = dict(
            attempts.values('question__topic')
            .annotate(count=Count('id'), solved=Count('id', filter=Q(is_solved=True)))
        )
        
        # Recent activity (last 7 days)
        week_ago = timezone.now() - timedelta(days=7)
        recent_activity = list(
            attempts.filter(last_attempted_at__gte=week_ago)
            .dates('last_attempted_at', 'day')
            .values('date')
            .annotate(count=Count('id'))
        )
        
        return {
            'total_attempted': attempts.count(),
            'total_solved': attempts.filter(is_solved=True).count(),
            'accuracy': (attempts.filter(is_solved=True).count() / attempts.count() * 100) if attempts.exists() else 0,
            'by_difficulty': difficulty_breakdown,
            'by_topic': topic_breakdown,
            'recent_activity': recent_activity,
        }

    def _get_aptitude_stats(self, user):
        """Get detailed aptitude statistics"""
        attempts = AptitudeAttempt.objects.filter(user=user)
        
        # By category
        category_breakdown = {}
        for category in ['Time and Work', 'Time and Distance', 'Probability', 'Percentages', 'Logical Reasoning']:
            cat_attempts = attempts.filter(question__category=category)
            cat_correct = cat_attempts.filter(is_correct=True).count()
            category_breakdown[category] = {
                'attempted': cat_attempts.count(),
                'correct': cat_correct,
                'accuracy': (cat_correct / cat_attempts.count() * 100) if cat_attempts.exists() else 0
            }
        
        return {
            'total_attempted': attempts.count(),
            'total_correct': attempts.filter(is_correct=True).count(),
            'overall_accuracy': (attempts.filter(is_correct=True).count() / attempts.count() * 100) if attempts.exists() else 0,
            'by_category': category_breakdown,
        }

    def _get_company_stats(self, user):
        """Get company preparation progress"""
        # This is a simplified version - in production, you'd track which companies user viewed/prepared
        total_companies = Company.objects.count()
        prepared_companies = 0  # Would need a CompanyPrep model to track this
        
        return {
            'total_companies': total_companies,
            'prepared_companies': prepared_companies,
            'completion_percentage': (prepared_companies / total_companies * 100) if total_companies > 0 else 0,
        }

    def _get_roadmap_stats(self, user):
        """Get roadmap progress statistics"""
        items = RoadmapItem.objects.filter(user=user)
        
        status_breakdown = {
            'not_started': items.filter(status='Not Started').count(),
            'in_progress': items.filter(status='In Progress').count(),
            'completed': items.filter(status='Completed').count(),
        }
        
        # By category
        category_breakdown = dict(
            items.values('category')
            .annotate(total=Count('id'), completed=Count('id', filter=Q(status='Completed')))
        )
        
        return {
            'total_items': items.count(),
            'status_breakdown': status_breakdown,
            'completion_percentage': (status_breakdown['completed'] / items.count() * 100) if items.exists() else 0,
            'by_category': category_breakdown,
        }

    def _get_recent_activity(self, user):
        """Get recent activity across all modules"""
        activities = []
        
        # Recent coding activity
        coding_activities = CodingProgress.objects.filter(user=user).order_by('-last_attempted_at')[:5]
        for activity in coding_activities:
            activities.append({
                'type': 'coding',
                'description': f'Solved {activity.question.title}' if activity.is_solved else f'Attempted {activity.question.title}',
                'timestamp': activity.last_attempted_at.isoformat(),
                'icon': 'code'
            })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return activities[:10]  # Return top 10 recent activities


class UpdateProgressView(views.APIView):
    """API endpoint to manually update progress (for integration with other modules)"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Update user progress based on activity"""
        progress, _ = UserProgress.objects.get_or_create(user=request.user)
        
        activity_type = request.data.get('type')
        
        if activity_type == 'coding_attempt':
            progress.coding_attempted += 1
            progress.last_coding_activity = timezone.now()
        elif activity_type == 'coding_solved':
            progress.coding_solved += 1
        elif activity_type == 'mock_completed':
            progress.mock_interviews_completed += 1
            score = request.data.get('score', 0)
            # Update average score
            total_sessions = progress.mock_interviews_completed
            progress.mock_interviews_average_score = (
                (progress.mock_interviews_average_score * (total_sessions - 1) + score) / total_sessions
            )
            progress.last_mock_activity = timezone.now()
        elif activity_type == 'aptitude_attempt':
            progress.aptitude_attempted += 1
            progress.last_aptitude_activity = timezone.now()
        elif activity_type == 'aptitude_correct':
            progress.aptitude_correct += 1
        
        progress.save()
        
        return Response({'status': 'Progress updated successfully'})
