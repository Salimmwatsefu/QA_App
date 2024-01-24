from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from .permissions import IsAnswerAuthor, CanAnswerQuestionOnlyByOthers

class ListQuestionsView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the author field to the authenticated user
        serializer.save(author=self.request.user)

class RetrieveUpdateDestroyQuestionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        # Ensure that only the author of the question can delete it
        if instance.author != self.request.user:
            raise PermissionError("You do not have permission to delete this question.")
        instance.delete()
        return Response({"message": "Question deleted successfully."}, status=200)

#Answers
        

class ListCreateAnswersView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated, CanAnswerQuestionOnlyByOthers]

    def get_queryset(self):
        question_id = self.kwargs.get('question_id')
        return Answer.objects.filter(question_id=question_id)

    def perform_create(self, serializer):
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, pk=question_id)
        serializer.save(question=question, author=self.request.user)

class RetrieveUpdateDestroyAnswerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated, IsAnswerAuthor]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)




