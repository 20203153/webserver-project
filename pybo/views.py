from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from pybo.models import Question, Answer, QuestionTopic
from pybo.serializers import QuestionSerializer, QuestionListSerializer, AnswerSerializer, QuestionTopicSerializer
from users.permissions import CustomReadOnly


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class QuestionListAPI(ListAPIView):
    queryset = Question.objects.all().order_by('-id')
    serializer_class = QuestionListSerializer
    pagination_class = StandardResultsSetPagination


class QuestionCreateAPI(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [CustomReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailAPI(APIView):
    serializer_class = QuestionSerializer
    permission_classes = [CustomReadOnly]

    def get(self, request, question_id=None, *args, **kwargs):
        qid = question_id or self.kwargs.get('question_id')
        if id:
            question = get_object_or_404(Question, id=qid)
            question.hit += 1
            question.save()

            serializer = QuestionSerializer(question)
        else:
            serializer = QuestionSerializer()
        return Response(serializer.data)

    def put(self, request, question_id=None, *args, **kwargs):
        qid = question_id or self.kwargs.get('question_id')
        question = get_object_or_404(Question, id=qid)

        serializer = QuestionSerializer(data=request.data, instance=question)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id=None, *args, **kwargs):
        qid = question_id or self.kwargs.get('question_id')
        question = get_object_or_404(Question, id=qid)

        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerDetailAPI(APIView):
    serializer_class = AnswerSerializer
    permission_classes = [CustomReadOnly]

    def get(self, request, answer_id=None, *args, **kwargs):
        aid = answer_id or self.kwargs.get('answer_id')
        if id:
            answer = get_object_or_404(Answer, id=aid)
            serializer = AnswerSerializer(answer)
        else:
            serializer = QuestionSerializer()
        return Response(serializer.data)

    def put(self, request, question_id=None, answer_id=None, *args, **kwargs):
        qid = question_id or self.kwargs.get('question_id')
        aid = answer_id or self.kwargs.get('answer_id')
        answer = get_object_or_404(Answer, question=qid, id=aid)

        serializer = AnswerSerializer(data=request.data, instance=answer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id=None, answer_id=None, *args, **kwargs):
        qid = question_id or self.kwargs.get('question_id')
        aid = answer_id or self.kwargs.get('answer_id')
        answer = get_object_or_404(Answer, question=qid, id=aid)

        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerCreateAPI(APIView):
    serializer_class = AnswerSerializer
    permission_classes = [CustomReadOnly]

    def post(self, request, question_id=None, *args, **kwargs):
        qid = question_id or self.kwargs.get('question_id')
        question = get_object_or_404(Question, id=qid)

        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question_id=question.id, owner_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicListAPI(ListAPIView):
    queryset = QuestionTopic.objects.all()
    serializer_class = QuestionTopicSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = QuestionTopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TopicAPI(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionTopicSerializer

    def get(self, request, topic_id=None, *args, **kwargs):
        tid = topic_id or self.kwargs.get('topic_id')
        topic = get_object_or_404(QuestionTopic, id=tid)
        if topic:
            serializer = QuestionTopicSerializer(topic)
        else:
            serializer = QuestionTopicSerializer()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, topic_id=None, *args, **kwargs):
        serializer = QuestionTopicSerializer(data=request.data)
        tid = topic_id or self.kwargs.get('topic_id')
        topic = get_object_or_404(QuestionTopic, id=tid)

        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)