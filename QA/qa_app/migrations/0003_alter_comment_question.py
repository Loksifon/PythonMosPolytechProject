# Generated by Django 4.0.10 on 2023-06-29 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa_app', '0002_alter_comment_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa_app.question'),
        ),
    ]
