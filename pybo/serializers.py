from rest_framework import serializers

from pybo.models import Question, Answer, QuestionTopic


class QuestionTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTopic
        fields = 'content',


class QuestionListSerializer(serializers.ModelSerializer):
    topic = serializers.StringRelatedField(many=True, read_only=True)
    owner = serializers.StringRelatedField(source='owner.profile.nickname', read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Question
        fields = 'id', 'subject', 'created_at', 'updated_at', 'topic', 'owner', 'owner_id', 'hit'


class AnswerSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(source='owner.profile.nickname', read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(source='owner.profile.nickname', read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    answer = AnswerSerializer(many=True, source='answer_set', read_only=True)
    topic = serializers.SlugRelatedField(slug_field='content', many=True, queryset=QuestionTopic.objects)

    class Meta:
        model = Question
        fields = ('id', 'subject', 'content', 'created_at', 'updated_at',
                  'topic', 'owner', 'owner_id', 'answer', 'hit')
