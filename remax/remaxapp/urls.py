from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    
    path('company/create/',views.create_company, name='create_company'),
    path('company/lists/',views.company_lists, name='company_lists'),
    path('company/update/<int:company_id>/', views.update_company, name='update_company'),  # Şirket güncelleme
    path('company/delete/<int:company_id>/', views.delete_company, name='delete_company'),
    path('company/reload/<int:company_id>/', views.reload_company, name='reload_company'),

    path('presentation/create/',views.presentation_create, name='presentation_create'),
    path('presentation/lists/',views.presentation_lists, name='presentation_lists'),
    path('presentation/update/<int:presentation_id>/', views.update_presentation, name='update_presentation'),  # Şirket güncelleme
    path('presentation/delete/<int:presentation_id>/', views.delete_presentation, name='delete_presentation'),
    path('presentation/reload/<int:presentation_id>/', views.reload_presentation, name='reload_presentation'),

    path('question/create/<int:presentation_id>/',views.question_create, name='question_create'),
    path('question/lists/',views.question_lists, name='question_lists'),
    path('question/update/<int:question_id>/', views.update_question, name='update_question'),  # Şirket güncelleme
    path('question/delete/<int:question_id>/', views.delete_question, name='delete_question'),
    path('question/reload/<int:question_id>/', views.reload_question, name='reload_question'),

    path('classroom/select/company/', views.create_classroom_company, name='create_classroom_company'),
    path('classroom/select/presentation/<int:company_id>/',views.select_presentation, name='select_presentation'),
    path('classroom/create/<int:company_id>/<int:presentation_id>/', views.create_classroom, name='create_classroom'),
    path('classroom/qrcode/<int:classroom_id>/<int:presentation_id>/',views.base, name='base'),
    path('classroom/join/<str:classroom_code>/<int:presentation_id>/',views.join_classroom, name='join_classroom'),
    path('classroom/quest/<str:participant_id>/<int:question_id>/',views.classroom_quest, name='classroom_quest'),

    path('karne/<str:participant_id>/<int:presentation_id>/',views.karne, name='karne'),


]
