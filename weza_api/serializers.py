from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Question, Answer

class QuestionSerializer(serializers.ModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'author', 'author_username', 'content', 'created_at']

    def get_author_username(self, obj):
        return obj.author.username if obj.author else None




class AnswerSerializer(serializers.ModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    author_id = serializers.ReadOnlyField(source='author.id')
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Answer
        fields = ['id', 'question', 'author', 'author_id', 'author_username', 'content', 'created_at']
        read_only_fields = ['question']

        def validate(self, data):
        # Automatically set the question based on the URL parameter
         question_id = self.context['view'].kwargs.get('question_id')
         question = get_object_or_404(Question, pk=question_id)
         data['question'] = question
         return data
        
    
