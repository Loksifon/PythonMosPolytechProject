# Generated by Django 4.0.10 on 2023-06-29 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa_app', '0003_alter_comment_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='question',
        ),
    ]