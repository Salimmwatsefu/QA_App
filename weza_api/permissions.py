from rest_framework import permissions
from .models import Question

class IsAnswerAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
    
class CanAnswerQuestionOnlyByOthers(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the request method is POST (answering a question)
        if request.method == 'POST':
            # Check if the author of the question is not the same as the current user
            question_id = view.kwargs.get('question_id')
            question = Question.objects.get(pk=question_id)
            
            return question.author != request.user
        return True  # For other methods, allow the permission
