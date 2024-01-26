from django import forms
from import_export import resources, fields, widgets
from django.contrib import admin
from .models import Category, Question, Answer, Comment, Tag
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponse
from import_export.formats import base_formats
from import_export import resources
from .models import Answer, Category, Question

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class AnswerResource(resources.ModelResource):
    class Meta:
        model = Answer


class CategoryResource(resources.ModelResource):
    about_category = fields.Field(
        column_name='Теги',
        attribute='get_about_category',
        widget=widgets.CharWidget(),
    )

    combined_info = fields.Field(
        column_name='Комбинированная Информация',
        attribute='get_combined_info',
        widget=widgets.CharWidget(),
    )

    class Meta:
        model = Category
        fields = ('id', 'name', 'about_category')

    def dehydrate_about_category(self, category):
        tags = Tag.objects.filter(categories=category)
        tag_names = [tag.name for tag in tags]
        tag_count = len(tag_names)
        return f"{', '.join(tag_names)} ({tag_count} {'тег' if tag_count == 1 else 'тегов'})"



class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question

    description = fields.Field(column_name='Description')

    def dehydrate_description(self, question):
        return f'Вопрос "{question.title}" Содержит ответов: {question.answers.count()}'

class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'display_tags', )
    list_filter = ('name',)
    search_fields = ('name',)
    formats = [base_formats.XLS, base_formats.XLSX, base_formats.CSV]

    def display_tags(self, obj):
        tags = Tag.objects.filter(categories=obj)
        return ",".join([tag.name for tag in tags])

    display_tags.short_description = 'Теги'
    

    resource_class = CategoryResource

class QuestionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('title', 'author', 'created_at', 'tags')
    search_fields = ('title', 'author__username')
    formats = [base_formats.XLS, base_formats.XLSX, base_formats.CSV]
    fieldsets = (
        ('Question Information', {
            'fields': ('title', 'author')
        }),
        ('Tag Information', {
            'fields': ('tags',)
        }),
    )

    resource_class = QuestionResource





class AnswerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('question', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('question__title', 'author__username')
    formats = [base_formats.XLS, base_formats.XLSX, base_formats.CSV]



class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    formats = [base_formats.XLS, base_formats.XLSX, base_formats.CSV]
    list_display = ('content', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('content', 'author__username',)



class TagAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    formats = [base_formats.XLS, base_formats.XLSX, base_formats.CSV]
    list_display = ('name', 'display_questions')


    def display_questions(self, obj):
        return ", ".join([question.title for question in obj.questions.all()])

    display_questions.short_description = 'Вопросы'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
