from django.db import models


class QuestionAnswerHistory(models.Model):
    question = models.TextField()

    answer = models.TextField()

    retrieved_chunks = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]
