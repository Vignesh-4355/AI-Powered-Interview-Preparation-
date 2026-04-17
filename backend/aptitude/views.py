from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import AptitudeQuestion, UserAttempt
from .serializers import (
    AptitudeQuestionSerializer,
    AptitudeQuestionListSerializer,
   UserAttemptSerializer
)


class AptitudeQuestionViewSet(viewsets.ModelViewSet):
    """
   ViewSet for viewing aptitude questions.
    
    Actions:
    - list: GET /api/aptitude/ - List all questions (filterable by category)
    - retrieve: GET /api/aptitude/{id}/ - Get question details
    - by_category: GET /api/aptitude/{category}/ - Get questions by category
    - submit_answer: POST /api/aptitude/{id}/submit_answer/ - Submit answer
    """
    queryset = AptitudeQuestion.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return AptitudeQuestionListSerializer
        return AptitudeQuestionSerializer

    def get_queryset(self):
        queryset = AptitudeQuestion.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset

    @action(detail=False, methods=['get'])
    def by_category(self, request, category=None):
        """Get questions by specific category"""
        category = request.query_params.get('category', self.kwargs.get('category'))
        if not category:
            return Response(
                {'error': 'Category required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        questions = self.get_queryset().filter(category=category)
        serializer = self.get_serializer(questions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        """Submit answer for a question"""
        question = self.get_object()
        selected_answer = request.data.get('selected_answer')
        time_taken = request.data.get('time_taken')
        
        if not selected_answer:
            return Response(
                {'error': 'Selected answer required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_correct = str(selected_answer).lower() == str(question.correct_answer).lower()
        
        # Track attempt if user authenticated
        if request.user.is_authenticated:
            UserAttempt.objects.update_or_create(
                user=request.user,
                question=question,
                defaults={
                    'selected_answer': selected_answer,
                    'is_correct': is_correct,
                    'time_taken': time_taken
                }
            )
        
        return Response({
            'is_correct': is_correct,
            'correct_answer': question.correct_answer if not is_correct else None,
            'solution': question.solution,
            'explanation': question.explanation
        })


class UserAttemptViewSet(viewsets.ModelViewSet):
    """
   ViewSet for managing user attempts.
    
    Actions:
    - list: GET /api/user-attempts/ - Get user's attempts
    - stats: GET /api/user-attempts/stats/ - Get user statistics
    """
    serializer_class = UserAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAttempt.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user's aptitude statistics"""
        queryset = self.get_queryset()
        total_attempts = queryset.count()
        correct_count = queryset.filter(is_correct=True).count()
        accuracy = (correct_count / total_attempts * 100) if total_attempts > 0 else 0
        
        # Stats by category
        category_stats = {}
        for category in ['Time and Work', 'Time and Distance', 'Probability', 'Percentages', 'Logical Reasoning']:
            cat_attempts = queryset.filter(question__category=category)
            cat_correct = cat_attempts.filter(is_correct=True).count()
            category_stats[category] = {
                'attempted': cat_attempts.count(),
                'correct': cat_correct,
                'accuracy': (cat_correct / cat_attempts.count() * 100) if cat_attempts.count() > 0 else 0
            }
        
        return Response({
            'total_attempts': total_attempts,
            'correct': correct_count,
            'accuracy': round(accuracy, 2),
            'by_category': category_stats
        })
