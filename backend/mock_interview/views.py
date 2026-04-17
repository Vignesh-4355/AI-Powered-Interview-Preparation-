"""
Views for Mock Interview Simulation Module
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
import random
from .models import InterviewQuestion, MockInterviewSession, UserAnswer
from .serializers import (
    InterviewQuestionSerializer,
    UserAnswerSerializer,
    MockInterviewSessionSerializer,
    SessionDetailSerializer,
)


class MockInterviewViewSet(viewsets.ViewSet):
    """
    ViewSet for managing mock interview sessions.
    
    Actions:
    - start: POST /api/mock/start/ - Start new interview session
    - answer: POST /api/mock/answer/ - Submit answer and get next question
    - result: GET /api/mock/result/{session_id}/ - Get session results
    - history: GET /api/mock/history/ - Get user's past interviews
    """
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def start(self, request):
        """Start a new mock interview session"""
        interview_type = request.data.get('interview_type', 'Mixed')
        difficulty = request.data.get('difficulty', 'Medium')
        total_questions = int(request.data.get('total_questions', 5))

        # Validate inputs
        if interview_type not in ['HR', 'Technical', 'Coding', 'Mixed']:
            return Response(
                {'error': 'Invalid interview type. Choose: HR, Technical, Coding, or Mixed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if difficulty not in ['Easy', 'Medium', 'Hard']:
            return Response(
                {'error': 'Invalid difficulty. Choose: Easy, Medium, or Hard'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create session
        session = MockInterviewSession.objects.create(
            user=request.user,
            interview_type=interview_type,
            difficulty=difficulty,
            total_questions=total_questions,
        )

        # Get first question
        question = self._get_next_question(session, [])
        
        if not question:
            return Response(
                {'error': 'No questions available for selected criteria'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            'session': MockInterviewSessionSerializer(session).data,
            'question': InterviewQuestionSerializer(question).data,
            'question_number': 1,
            'total_questions': total_questions,
        })

    @action(detail=False, methods=['post'])
    def answer(self, request):
        """Submit answer and get next question"""
        session_id = request.data.get('session_id')
        question_id = request.data.get('question_id')
        answer_text = request.data.get('answer_text', '')

        if not session_id or not question_id:
            return Response(
                {'error': 'session_id and question_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get session
        try:
            session = MockInterviewSession.objects.get(
                id=session_id,
                user=request.user
            )
        except MockInterviewSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if session.is_completed:
            return Response(
                {'error': 'Session already completed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get question
        try:
            question = InterviewQuestion.objects.get(id=question_id)
        except InterviewQuestion.DoesNotExist:
            return Response(
                {'error': 'Question not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if question already answered
        if UserAnswer.objects.filter(session=session, question=question).exists():
            return Response(
                {'error': 'Question already answered in this session'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Evaluate answer using keyword matching
        keyword_score, feedback = self._evaluate_answer(question, answer_text)

        # Save answer
        UserAnswer.objects.create(
            session=session,
            question=question,
            answer_text=answer_text,
            keyword_score=keyword_score,
            feedback=feedback,
        )

        # Get answered question IDs
        answered_ids = list(
            UserAnswer.objects.filter(session=session).values_list('question_id', flat=True)
        )

        # Check if all questions answered
        if len(answered_ids) >= session.total_questions:
            # Complete session
            session.end_time = timezone.now()
            session.is_completed = True
            
            # Calculate overall score
            answers = UserAnswer.objects.filter(session=session)
            avg_score = answers.aggregate(
                avg_score=Avg('keyword_score')
            )['avg_score'] or 0
            
            session.score = round(avg_score, 2)
            session.feedback = self._generate_session_feedback(session)
            session.save()

            return Response({
                'completed': True,
                'session': SessionDetailSerializer(session).data,
            })

        # Get next question
        next_question = self._get_next_question(session, answered_ids)

        if not next_question:
            # No more questions, complete session
            session.end_time = timezone.now()
            session.is_completed = True
            session.save()

            return Response({
                'completed': True,
                'session': SessionDetailSerializer(session).data,
            })

        return Response({
            'completed': False,
            'question': InterviewQuestionSerializer(next_question).data,
            'question_number': len(answered_ids) + 1,
            'total_questions': session.total_questions,
            'previous_feedback': feedback,
        })

    @action(detail=False, methods=['get'], url_path='result/(?P<session_id>[^/.]+)')
    def result(self, request, session_id=None):
        """Get detailed session results"""
        try:
            session = MockInterviewSession.objects.get(
                id=session_id,
                user=request.user
            )
        except MockInterviewSession.DoesNotExist:
            return Response(
                {'error': 'Session not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if not session.is_completed:
            return Response(
                {'error': 'Session not yet completed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(SessionDetailSerializer(session).data)

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get user's interview history"""
        sessions = MockInterviewSession.objects.filter(
            user=request.user,
            is_completed=True
        ).order_by('-start_time')

        return Response(
            MockInterviewSessionSerializer(sessions, many=True).data
        )

    def _get_next_question(self, session, answered_ids):
        """Get next random question based on session criteria"""
        # Build query based on interview type
        if session.interview_type == 'Mixed':
            questions = InterviewQuestion.objects.exclude(
                id__in=answered_ids
            )
        else:
            questions = InterviewQuestion.objects.filter(
                question_type=session.interview_type
            ).exclude(id__in=answered_ids)

        # Filter by difficulty
        if session.difficulty == 'Easy':
            questions = questions.filter(difficulty='Easy')
        elif session.difficulty == 'Medium':
            questions = questions.filter(
                difficulty__in=['Easy', 'Medium']
            )
        else:  # Hard
            questions = questions.filter(
                difficulty__in=['Easy', 'Medium', 'Hard']
            )

        # Return random question
        if questions.exists():
            return random.choice(questions)
        
        # Fallback: any unanswered question
        if answered_ids:
            return InterviewQuestion.objects.exclude(
                id__in=answered_ids
            ).first()
        
        return InterviewQuestion.objects.first()

    def _evaluate_answer(self, question, answer_text):
        """Evaluate answer using keyword matching"""
        if not answer_text.strip():
            return 0, "No answer provided."

        answer_lower = answer_text.lower()
        keywords = question.expected_keywords or []
        
        if not keywords:
            return 50, "Good attempt. Try to include more specific details."

        # Count matched keywords
        matched_keywords = [
            keyword for keyword in keywords
            if keyword.lower() in answer_lower
        ]
        
        matched_count = len(matched_keywords)
        total_keywords = len(keywords)
        
        # Calculate score (0-100)
        score = (matched_count / total_keywords) * 100 if total_keywords > 0 else 50
        score = min(score, 100)

        # Generate feedback
        if score >= 80:
            feedback = f"Excellent! You covered {matched_count}/{total_keywords} key points. Very comprehensive answer."
        elif score >= 60:
            feedback = f"Good attempt! You covered {matched_count}/{total_keywords} key points. Consider adding: {', '.join(keywords[:3])}"
        elif score >= 40:
            feedback = f"Fair attempt. You covered {matched_count}/{total_keywords} key points. Try to include more technical details."
        else:
            feedback = f"Needs improvement. You covered {matched_count}/{total_keywords} key points. Review the topic and try again."

        return round(score, 2), feedback

    def _generate_session_feedback(self, session):
        """Generate overall session feedback"""
        answers = UserAnswer.objects.filter(session=session)
        avg_score = answers.aggregate(
            avg_score=Avg('keyword_score')
        )['avg_score'] or 0

        if avg_score >= 80:
            return "Outstanding performance! You demonstrated strong knowledge and provided comprehensive answers. Keep up the excellent work!"
        elif avg_score >= 60:
            return "Good performance! You showed solid understanding. Focus on including more specific details and examples to improve further."
        elif avg_score >= 40:
            return "Fair attempt. You have basic understanding but need to deepen your knowledge. Review key concepts and practice more."
        else:
            return "Needs significant improvement. Focus on understanding fundamental concepts and practice regularly to build confidence."


# Import Avg for aggregation
from django.db.models import Avg


class InterviewQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing interview questions.
    
    Actions:
    - list: GET /api/mock/questions/ - List all questions
    - retrieve: GET /api/mock/questions/{id}/ - Get question details
    """
    queryset = InterviewQuestion.objects.all()
    serializer_class = InterviewQuestionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = InterviewQuestion.objects.all()
        
        # Filter by type
        question_type = self.request.query_params.get('type', None)
        if question_type:
            queryset = queryset.filter(question_type=question_type)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset
