from django.test import TestCase
from qa_app.forms import RegistrationForm, CommentForm, QuestionForm, AnswerForm


class RegistrationFormTest(TestCase):
    def test_form_fields(self):
        form = RegistrationForm()
        self.assertTrue('username' in form.fields)
        self.assertTrue('password1' in form.fields)
        self.assertTrue('password2' in form.fields)

    def test_form_widget_attrs(self):
        form = RegistrationForm()
        self.assertEqual(form.fields['username'].widget.attrs.get('class'), 'login__input')
        self.assertEqual(form.fields['password1'].widget.attrs.get('class'), 'login__input')
        self.assertEqual(form.fields['password2'].widget.attrs.get('class'), 'login__input')

    def test_form_help_text(self):
        form = RegistrationForm()
        self.assertEqual(form.fields['username'].help_text, '')
        self.assertEqual(form.fields['password1'].help_text, '')
        self.assertEqual(form.fields['password2'].help_text, '')


class CommentFormTest(TestCase):
    def test_form_fields(self):
        form = CommentForm()
        self.assertTrue('content' in form.fields)

    def test_form_widget_attrs(self):
        form = CommentForm()
        self.assertEqual(form.fields['content'].widget.attrs.get('rows'), 3)


class QuestionFormTest(TestCase):
    def test_form_fields(self):
        form = QuestionForm()
        self.assertTrue('title' in form.fields)
        self.assertTrue('content' in form.fields)
        self.assertTrue('tags' in form.fields)

    def test_form_widget_attrs(self):
        form = QuestionForm()
        self.assertEqual(form.fields['title'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['content'].widget.attrs.get('class'), 'form-control')
        self.assertEqual(form.fields['content'].widget.attrs.get('rows'), 3)
        self.assertEqual(form.fields['tags'].widget.attrs.get('class'), 'form-control')


class AnswerFormTest(TestCase):
    def test_form_fields(self):
        form = AnswerForm()
        self.assertTrue('content' in form.fields)

    def test_form_labels(self):
        form = AnswerForm()
        self.assertEqual(form.fields['content'].label, 'Ответ')

    def test_form_widget_attrs(self):
        form = AnswerForm()
        self.assertEqual(form.fields['content'].widget.attrs.get('rows'), 3)
