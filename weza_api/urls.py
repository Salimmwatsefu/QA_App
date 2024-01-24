from django.urls import path
from .views import ListQuestionsView, RetrieveUpdateDestroyQuestionView, ListCreateAnswersView, RetrieveUpdateDestroyAnswerView

urlpatterns = [
    path('questions/', ListQuestionsView.as_view(), name='list-questions'),
    path('questions/<int:pk>/', RetrieveUpdateDestroyQuestionView.as_view(), name='retrieve-update-destroy-question'),
    path('questions/<int:question_id>/answers/', ListCreateAnswersView.as_view(), name='list-create-answers'),
    path('questions/<int:question_id>/answers/<int:pk>/', RetrieveUpdateDestroyAnswerView.as_view(), name='retrieve-update-destroy-answer')
]
