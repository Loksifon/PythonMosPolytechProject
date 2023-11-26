# Generated by Django 4.2.2 on 2023-11-26 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa_app', '0007_alter_answer_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answers',
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='qa_app.question', verbose_name='Вопрос'),
        ),
    ]