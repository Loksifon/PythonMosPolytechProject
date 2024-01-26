from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'




class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='questions', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    tags = models.ManyToManyField('Tag', related_name='questions', verbose_name='Тэги')
    answers = models.ManyToManyField('Answer', related_name='question_answers', verbose_name='Ответы')
    is_favorite = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_set', verbose_name='Вопрос')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_authors', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    history = HistoricalRecords()

    def __str__(self):
        return f"Answer to {self.question.title}"

    class Meta:
        verbose_name_plural = 'Ответы'


class Comment(models.Model):
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"Comment by {self.author}"

    class Meta:
        verbose_name_plural = 'Комментарии'

        


class Tag(models.Model):
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='tags', verbose_name='Categories')

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Тэги'