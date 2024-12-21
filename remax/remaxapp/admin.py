from django.contrib import admin
from .models import Trainer, Company, Classroom, Presentation, Question, Participant, Answer

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_active', 'created_at', 'last_updated_at')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'phone')
    ordering = ('-created_at',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'last_updated_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('code', 'company', 'is_active', 'created_at', 'last_updated_at')
    list_filter = ('is_active', 'company')
    search_fields = ('code', 'company__name')
    ordering = ('-created_at',)


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'is_active', 'created_at', 'last_updated_at')
    list_filter = ('is_active', 'company')
    search_fields = ('name', 'company__name')
    ordering = ('-created_at',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('presentation', 'page', 'is_active', 'created_at', 'last_updated_at')
    list_filter = ('is_active', 'presentation')
    search_fields = ('presentation__name', 'question_text')
    ordering = ('-created_at',)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'is_active', 'created_at', 'last_updated_at')
    list_filter = ('is_active', 'company')
    search_fields = ('name', 'email', 'company__name')
    ordering = ('-created_at',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('participant', 'question', 'is_active', 'created_at', 'last_updated_at')
    list_filter = ('is_active', 'question', 'participant')
    search_fields = ('participant__name', 'question__question_text')
    ordering = ('-created_at',)
