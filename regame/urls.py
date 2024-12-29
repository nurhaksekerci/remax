from django.contrib import admin
from django.urls import path
from mainapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name="login"),
    path('register/', register, name="register"),
    path('index/', index, name="index"),

    path('list-company/', list_company, name='list_company'),
    path('create-company/', create_company, name='create_company'),
    path('update-company/<int:company_id>/', update_company, name='update_company'),
    path('delete-company/<int:company_id>/', delete_company, name='delete_company'),

    path('create-presentation/<int:company_id>/', create_presentation, name='create_presentation'),
    path('detail-presentation/<int:presentation_id>/', presentation_detail, name='presentation_detail'),
    path('update-presentation/<int:presentation_id>/', update_presentation, name='update_presentation'),
    path('delete-presentation/<int:presentation_id>/', delete_presentation, name='delete_presentation'),
    path('delete-question/<int:presentation_id>/<int:question_number>/', delete_question, name='delete_question'),

    path('create-classroom/', create_classroom, name="create_classroom"),
    path('create-classroom/<int:company_id>/', create_classroom_company, name="create_classroom_company"),
    path('create-classroom/<int:company_id>/<int:presentation_id>/', create_classroom_start, name="create_classroom_start"),
    path('join-classroom/<str:classroom_code>/', join_classroom, name="join_classroom"),
    path('answer-questions/<str:classroom_code>/<int:participant_id>/', questions, name="questions"),
    path('save-answers/<str:classroom_code>/<int:participant_id>/', save_answers, name="save_answers"),

    path('update_info/<str:classroom_code>/', update_info, name="update_info")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
