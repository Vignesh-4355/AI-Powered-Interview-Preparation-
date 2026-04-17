from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import CodingQuestion, UserProgress
from .serializers import (
    CodingQuestionSerializer,
    CodingQuestionListSerializer,
    UserProgressSerializer
)


class CodingQuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and interacting with coding questions.
    
    Actions:
    - list: GET /api/coding-questions/ - List all questions (with filters)
    - retrieve: GET /api/coding-questions/{id}/ - Get question details
    - mark_solved: POST /api/coding-questions/{id}/mark_solved/ - Mark as solved
    - bookmark: POST /api/coding-questions/{id}/bookmark/ - Bookmark question
    - remove_bookmark: POST /api/coding-questions/{id}/remove_bookmark/ - Remove bookmark
    """
    queryset = CodingQuestion.objects.all()
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return CodingQuestionListSerializer
        return CodingQuestionSerializer

    def get_queryset(self):
        """Filter questions by difficulty, topic, or search query"""
        queryset = CodingQuestion.objects.all()
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by topic
        topic = self.request.query_params.get('topic', None)
        if topic:
            queryset = queryset.filter(topic=topic)
        
        # Search by title
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(title__icontains=search)
        
        return queryset

    @action(detail=True, methods=['post'])
    def mark_solved(self, request, pk=None):
        """Mark a coding question as solved"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        question = self.get_object()
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            question=question
        )
        
        progress.is_solved = True
        progress.attempts += 1
        progress.last_attempted_at = timezone.now()
        progress.solved_at = timezone.now()
        progress.save()
        
        return Response({
            'message': 'Question marked as solved!',
            'is_solved': True
        })

    @action(detail=True, methods=['post'])
    def bookmark(self, request, pk=None):
        """Bookmark a coding question"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        question = self.get_object()
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            question=question
        )
        
        progress.is_bookmarked = True
        progress.save()
        
        return Response({
            'message': 'Question bookmarked!',
            'is_bookmarked': True
        })

    @action(detail=True, methods=['post'])
    def remove_bookmark(self, request, pk=None):
        """Remove bookmark from a coding question"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        question = self.get_object()
        try:
            progress = UserProgress.objects.get(
                user=request.user,
                question=question
            )
            progress.is_bookmarked = False
            progress.save()
            
            return Response({
                'message': 'Bookmark removed!',
                'is_bookmarked': False
            })
        except UserProgress.DoesNotExist:
            return Response({
                'message': 'Question was not bookmarked',
                'is_bookmarked': False
            })

    def retrieve(self, request, *args, **kwargs):
        """Get question details with user progress info"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)


class UserProgressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user progress.
    
    Actions:
    - list: GET /api/user-progress/ - Get user's progress
    - bookmarked: GET /api/user-progress/bookmarked/ - Get bookmarked questions
    - solved: GET /api/user-progress/solved/ - Get solved questions
    """
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get progress for the current user only"""
        return UserProgress.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def bookmarked(self, request):
        """Get all bookmarked questions for the user"""
        bookmarked = self.get_queryset().filter(is_bookmarked=True)
        serializer = self.get_serializer(bookmarked, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def solved(self, request):
        """Get all solved questions for the user"""
        solved = self.get_queryset().filter(is_solved=True)
        serializer = self.get_serializer(solved, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user's coding statistics"""
        queryset = self.get_queryset()
        total_questions = queryset.count()
        solved_count = queryset.filter(is_solved=True).count()
        bookmarked_count = queryset.filter(is_bookmarked=True).count()
        
        # Count by difficulty
        easy_solved = sum(1 for p in queryset if p.is_solved and p.question.difficulty == 'Easy')
        medium_solved = sum(1 for p in queryset if p.is_solved and p.question.difficulty == 'Medium')
        hard_solved = sum(1 for p in queryset if p.is_solved and p.question.difficulty == 'Hard')
        
        return Response({
            'total_attempted': total_questions,
            'solved': solved_count,
            'bookmarked': bookmarked_count,
            'by_difficulty': {
                'Easy': easy_solved,
                'Medium': medium_solved,
                'Hard': hard_solved
            }
        })
