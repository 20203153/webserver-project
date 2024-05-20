from django.contrib.auth.models import User
from django.db import models


class QuestionTopic(models.Model):
    content = models.CharField(max_length=10)

    def __str__(self):
        return f"#{self.content}"


class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    topic = models.ManyToManyField(QuestionTopic, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hit = models.IntegerField(default=0)
    voters = models.ManyToManyField(User, related_name="voter_question", blank=True)

    def __str__(self):
        return f"Question: {self.id} - {self.subject}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    voters = models.ManyToManyField(User, related_name="voter_answer", blank=True)

    def __str__(self):
        return f"Answer: {self.question_id} - {self.content}"
