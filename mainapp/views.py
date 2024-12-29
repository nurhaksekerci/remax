from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.forms.models import model_to_dict
import json
from django.http import JsonResponse
from django.contrib import messages

def login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Geçersiz kullanıcı adı veya şifre.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'pages/login.html', {'title': "Login", 'form_title': 'Login', 'form': form})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Kullanıcıyı otomatik giriş yap
            return redirect('home')  # Başarılı kayıt sonrası yönlendirilecek sayfa
    else:
        form = CustomUserCreationForm()
    return render(request, 'pages/register.html', {'title': "Kaydol", 'form_title': 'Kaydol', 'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})



def list_company(request):
    companies = Company.objects.all().values()
    return render(request, 'pages/list.html', {'data': companies, 'list_title': 'Şirket Listesi'})

def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.is_active = not company.is_active
    company.save()

    # Şirket verilerini düzenle
    company_data = model_to_dict(company)

    # Logo alanını kontrol et
    logo_url = company.logo.url if company.logo else None
    month_map = {
        "January": "Ocak", "February": "Şubat", "March": "Mart",
        "April": "Nisan", "May": "Mayıs", "June": "Haziran",
        "July": "Temmuz", "August": "Ağustos", "September": "Eylül",
        "October": "Ekim", "November": "Kasım", "December": "Aralık",
    }
    # Tarihleri formatla
    created_at = company.created_at.strftime("%d %B %Y %H:%M") if company.created_at else None
    last_updated_at = company.last_updated_at.strftime("%d %B %Y %H:%M") if company.last_updated_at else None

    if created_at:
        for eng, tr in month_map.items():
            created_at = created_at.replace(eng, tr)

    if last_updated_at:
        for eng, tr in month_map.items():
            last_updated_at = last_updated_at.replace(eng, tr)
    # values listesini oluştur
    company_data['values'] = [
        company.id,
        company.name,
        logo_url,
        created_at,
        last_updated_at,
        True if company.is_active else False,
    ]

    return render(request, 'includes/company-tr.html', {'obj': company_data})

@login_required
def update_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('list_company')  # Güncelleme sonrası yönlendirme yapılacak sayfa
    else:
        form = CompanyForm(instance=company)
    
    return render(request, 'pages/register.html', {
        'title': 'Şirket Güncelle',
        'form_title': 'Şirket Bilgilerini Güncelle',
        'form': form
    })



@login_required
def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save()
            return redirect('list_company')  # Oluşturma sonrası yönlendirme yapılacak sayfa
    else:
        form = CompanyForm()
    
    return render(request, 'pages/register.html', {
        'title': 'Yeni Şirket Oluştur',
        'form_title': 'Şirket Bilgilerini Gir',
        'form': form
    })

@login_required
def create_presentation(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    presentations = Presentation.objects.filter(company=company).order_by("-is_active")
    if request.method == 'POST':
        form = PresentationForm(request.POST, request.FILES)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.company = company
            presentation.save()
            return redirect('presentation_detail', presentation_id=presentation.id)  # Oluşturma sonrası yönlendirme
    else:
        form = PresentationForm()
    
    return render(request, 'pages/sunum.html', {
        'title': f'{company.name.capitalize()} İçin Yeni Sunum Oluştur',
        'list_title': f'{company.name.capitalize()} İçin Kayıtlı Sunumlar',
        'form_title': f'{company.name.capitalize()} İçin Sunum Bilgilerini Gir',
        'form': form,
        'presentations': presentations,
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

import json

def presentation_detail(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)

    # Soruları JSON'dan listeye dönüştür
    existing_questions = presentation.questions
    if isinstance(existing_questions, str):
        existing_questions = json.loads(existing_questions)
    elif not existing_questions:
        existing_questions = []

    # Varsayılan değerlerle soruları kontrol et
    for question in existing_questions:
        question.setdefault('question_number', None)
        question.setdefault('question_text', "Bilinmeyen soru")

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            updated_questions = form.save_to_json(existing_questions)
            presentation.questions = updated_questions
            presentation.save()
            return redirect('presentation_detail', presentation_id=presentation.id)
    else:
        form = QuestionForm()

    return render(request, 'pages/soru.html', {
        'title': f'{presentation.company.name} Şirketinin {presentation.name.capitalize()} Sunumu İçin Yeni Soru Oluştur',
        'form_title': f'{presentation.company.name} Şirketinin {presentation.name.capitalize()} Sunumu İçin Yeni Soru Oluştur',
        'form': form,
        'presentation': presentation,
        'questions': existing_questions,
    })



def delete_question(request, presentation_id, question_number):
    presentation = get_object_or_404(Presentation, id=presentation_id)

    # Soruları JSON'dan listeye dönüştür
    existing_questions = presentation.questions
    if isinstance(existing_questions, str):
        existing_questions = json.loads(existing_questions)
    elif not existing_questions:
        existing_questions = []

    # Soruyu sil
    updated_questions = [q for q in existing_questions if q.get('question_number') != question_number]

    # Güncellenmiş soruları kaydet
    presentation.questions = json.dumps(updated_questions)
    presentation.save()

    # İsteğin türüne göre yanıt döndür
    if request.headers.get('HX-Request'):  # HTMX isteği kontrolü
        return JsonResponse({'success': True})
    return redirect('presentation_detail', presentation_id=presentation.id)


@login_required
def update_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    
    if request.method == 'POST':
        form = PresentationForm(request.POST, request.FILES, instance=presentation)
        if form.is_valid():
            form.save()
            return redirect('presentation_detail', presentation_id=presentation.id)  # Güncelleme sonrası yönlendirme
    else:
        form = PresentationForm(instance=presentation)
    
    return render(request, 'pages/register.html', {
        'title': 'Sunumu Güncelle',
        'form_title': 'Sunum Bilgilerini Güncelle',
        'form': form
    })

@login_required
def delete_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    presentation.is_active = not presentation.is_active
    presentation.save()
    return redirect('create_presentation', company_id=presentation.company.id)

@login_required
def home(request):
    return render(request, 'pages/404.html', {'title': "TEst"})



def create_classroom(request):
    company = Company.objects.filter(is_active=True)
    return render(request, 'pages/create_classroom.html', {'title': "Sınıf Oluştur", 'list_title': 'Sınıf Oluşturmak İçin Şirket Seç', 'data':company})

def create_classroom_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    presentations = Presentation.objects.filter(company=company, is_active=True)
    return render(request, 'includes/presentetion.html', {'title': "TEst", 'data':presentations})

import qrcode
import uuid
from io import BytesIO
from django.core.files.base import ContentFile

def create_classroom_start(request, company_id, presentation_id):
    company = get_object_or_404(Company, id=company_id)
    presentation = get_object_or_404(Presentation, id=presentation_id)

    # Classroom oluştur
    classroom = Classroom.objects.create(
        company=company,
        presentation=presentation,
        code=f"{uuid.uuid4().hex[:8]}",  # Unique code with UUID
    )

    # QR kodu oluştur
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    unique_data = f"http://127.0.0.1:8000/classroom/{classroom.code}/"  # Add unique UUID to QR data
    qr.add_data(unique_data)
    qr.make(fit=True)

    # QR kodu bir resim olarak kaydet
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    classroom.qr_image.save(f"{classroom.code}.png", ContentFile(buffer.read()), save=True)
    buffer.close()

    return render(request, 'pages/classroom.html', {'title': "Classroom Created", 'classroom': classroom})

def join_classroom(request, classroom_code):
    print("############### join_classroom view çağrıldı ###############")
    classroom = get_object_or_404(Classroom, code=classroom_code, is_active=True)
    print(f"Sınıf bulundu: {classroom}")

    if request.method == 'POST':
        print("POST isteği alındı")
        form = ParticipantForm(request.POST)
        
        if form.is_valid():
            print("form doğru")
            email = form.cleaned_data.get('email')
            
            participant = Participant.objects.filter(email=email).first()
            if participant:
                messages.success(request, "Kullanıcı var")
            else:
                participant = form.save(commit=False)
                participant.classroom = classroom
                participant.save()
            
            classroom.participants.add(participant)
            classroom.save()
            toplam = classroom.participants.count()
            print(f'Toplammmmmmmmmmmmmmmmmmmmmmmmm {toplam}')
            return redirect('questions', classroom_code=classroom_code, participant_id=participant.id)
        else:
            email = form.data.get('email')
            participant = Participant.objects.filter(email=email).first()
            if participant:
                classroom.participants.add(participant)
                classroom.save()
                return redirect('questions', classroom_code=classroom_code, participant_id=participant.id)
            messages.error(request, "Formda hata var. Lütfen tekrar deneyin.")
    else:
        form = ParticipantForm()

    print("Form render ediliyor")
    return render(request, 'pages/register.html', {
        'title': "Sınıfa Katıl",
        'form_title': 'Seni Tanıyor Muyuz?',
        'form': form
    })

def questions(request, classroom_code, participant_id):
    classroom = get_object_or_404(Classroom, code=classroom_code)
    participant = get_object_or_404(Participant, id=participant_id)
    
    try:
        # JSON stringini Python listesine dönüştür
        questions = json.loads(classroom.presentation.questions)
        print(questions[0]['question_text'])
    except (json.JSONDecodeError, IndexError, TypeError) as e:
        questions = []
        print("Sorular yüklenemedi:", e)
    
    return render(request, 'pages/questions.html', {
        'title': "Sınıfa Katıl",
        'classroom': classroom,
        'form_title': 'Seni Tanıyor Muyuz?',
        'questions': questions,
        'participant': participant,
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def save_answers(request, classroom_code, participant_id):
    if request.method == "POST":
        classroom = get_object_or_404(Classroom, code=classroom_code)
        participant = get_object_or_404(Participant, id=participant_id)
        presentation = classroom.presentation
        try:
            # JSON verisini ayrıştır
            data = json.loads(request.body)
            answers_data = data.get("answers", [])

            # Cevapları JSON formatında kaydet
            Answer.objects.create(
                participant=participant,
                presentation=presentation,
                classroom=classroom,
                answers=answers_data,
            )

            return JsonResponse({"message": "Yanıtlar başarıyla kaydedildi."}, status=200)
        except Classroom.DoesNotExist:
            return JsonResponse({"error": "Geçersiz Classroom ID."}, status=400)
        except Participant.DoesNotExist:
            return JsonResponse({"error": "Geçersiz Participant ID."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Sadece POST isteklerine izin verilir."}, status=405)



from django.db.models import Count

def update_info(request, classroom_code):
    classroom = get_object_or_404(Classroom, code=classroom_code, is_active=True)

    toplam = classroom.participants.count()
    bitiren = Answer.objects.filter(classroom=classroom).aggregate(
        unique_participants=Count('participant', distinct=True)
    )['unique_participants']

    return render(request, 'includes/katilimci_detay.html',{
        'toplam': toplam,
        'bitiren': bitiren
    })


def index(requset):
    return render(requset, 'pages/anasayfa.html')