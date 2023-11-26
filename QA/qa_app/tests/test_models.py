from django.test import TestCase
from django.contrib.auth.models import User
from qa_app.models import Category, Question, Answer, Comment, Tag


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_str_representation(self):
        self.assertEqual(str(self.category), 'Test Category')


class QuestionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.question = Question.objects.create(title='Test Question', content='Test Content', author=self.user)
        self.question.tags.set([Tag.objects.create(name='Test Tag')])

    def test_str_representation(self):
        self.assertEqual(str(self.question), 'Test Question')


class AnswerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.question = Question.objects.create(
            title='Test Question',
            content='This is a test question.',
            author=self.user,
        )
        self.answer = Answer.objects.create(
            question=self.question,
            content='This is a test answer.',
            author=self.user,
        )

    def test_str_representation(self):
        self.assertEqual(str(self.answer), 'Answer to Test Question')


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.comment = Comment.objects.create(
            content='This is a test comment.',
            author=self.user,
        )

    def test_str_representation(self):
        self.assertEqual(str(self.comment), 'Comment by testuser')


class TagModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')
        self.tag.categories.set([self.category])
        # Используйте метод set() для установки связи many-to-many

    def test_str_representation(self):
        self.assertEqual(str(self.tag), 'Test Tag')
