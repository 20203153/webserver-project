from rest_framework import serializers

from pybo.models import Question, Answer


class QuestionListSerializer(serializers.ModelSerializer):
    topic = serializers.StringRelatedField(many=True)
    question_owner = serializers.StringRelatedField(source='question_owner.profile.nickname', read_only=True)
    question_owner_id = serializers.IntegerField(source='question_owner.id', read_only=True)

    class Meta:
        model = Question
        fields = 'id', 'subject', 'created_at', 'updated_at', 'topic', 'question_owner', 'question_owner_id'


class AnswerSerializer(serializers.ModelSerializer):
    answer_owner = serializers.StringRelatedField(source='answer_owner.profile.nickname', read_only=True)
    answer_owner_id = serializers.IntegerField(source='answer_owner.id', read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    question_owner = serializers.StringRelatedField(source='question_owner.profile.nickname', read_only=True)
    question_owner_id = serializers.IntegerField(source='question_owner.id', read_only=True)

    answer = AnswerSerializer(many=True, source='answer_set', read_only=True)
    topic = serializers.StringRelatedField(many=True)

    class Meta:
        model = Question
        fields = ('id', 'subject', 'content', 'created_at', 'updated_at',
                  'topic', 'question_owner', 'question_owner_id', 'answer')
