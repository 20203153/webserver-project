from rest_framework import serializers

from pybo.models import Question, Answer, QuestionTopic


class QuestionTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionTopic
        fields = 'content',


class QuestionListSerializer(serializers.ModelSerializer):
    topic = serializers.SlugRelatedField(slug_field='content', many=True, read_only=True)
    owner = serializers.StringRelatedField(source='owner.profile.nickname', read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    answers = serializers.IntegerField(source='answer_set.count', read_only=True)
    vote = serializers.IntegerField(source='voters.count', read_only=True)

    class Meta:
        model = Question
        fields = 'id', 'subject', 'created_at', 'updated_at', 'topic', 'owner', 'owner_id', 'hit', 'answers', 'vote'


class AnswerSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(source='owner.profile.nickname', read_only=True)
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    vote = serializers.IntegerField(source='voters.count', read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'


class SlugRelatedGetOrCreateField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get_or_create(**{self.slug_field: data})[0]
        except (TypeError, ValueError):
            self.fail("invalid")


class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(source='owner.profile.nickname', read_only=True)
    answer = AnswerSerializer(many=True, source='answer_set', read_only=True)
    hit = serializers.IntegerField(read_only=True)
    topic = SlugRelatedGetOrCreateField(
        slug_field='content', many=True, queryset=QuestionTopic.objects.all()
    )
    vote = serializers.IntegerField(source='voters.count', read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'subject', 'content', 'created_at', 'updated_at',
                  'topic', 'owner', 'owner_id', 'answer', 'hit', 'vote')