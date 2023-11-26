from django import forms
from django.contrib import admin
from .models import Category, Question, Answer, Comment, Tag

from import_export.admin import ImportExportModelAdmin


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'display_tags')
    list_filter = ('name',)
    search_fields = ('name',)
  

    def display_tags(self, obj):
        tags = Tag.objects.filter(categories=obj)
        return ", ".join([tag.name for tag in tags])

    display_tags.short_description = 'Теги'


class QuestionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('title', 'author', 'created_at', 'tags')
    search_fields = ('title', 'author__username')



class AnswerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('question', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('question__title', 'author__username')



class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('content', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('content', 'author__username',)



class TagAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'display_questions')


    def display_questions(self, obj):
        return ", ".join([question.title for question in obj.questions.all()])

    display_questions.short_description = 'Вопросы'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
