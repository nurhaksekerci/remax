from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
def base(request, classroom_id, presentation_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    presentation = get_object_or_404(Presentation, id=presentation_id)
    companies = Company.objects.filter(is_active=True)


    return render(request, 'base.html', {'show_navbar': True, 'classroom': classroom, 'presentation': presentation, 'companies': companies})

def join_classroom(request, classroom_code, presentation_id):
    classroom = get_object_or_404(Classroom, code=classroom_code)
    presentation = get_object_or_404(Presentation, id=presentation_id)
    question = Question.objects.filter(presentation=presentation).order_by("page").first()
    form = ParticipantForm()
    if request.method == "POST":
        form = ParticipantForm(request.POST)  # Doğru şekilde POST verilerini form ile bağla
        if form.is_valid():  # Formu doğrula
            new_obj = form.save(commit=False)
            new_obj.company = classroom.company  # classroom'un tanımlı olduğundan emin olun
            new_obj.save()  # Veritabanına kaydet
            messages.success(request, "Katılımcı başarıyla oluşturuldu!")
            return redirect('classroom_quest', participant_id=new_obj.id, question_id=question.id) 
    context = {
        'form': form,
        'title' : 'Seni tanıyor muyuz?'
    }

    return render(request, "kisi.html", context)

def classroom_quest(request, participant_id, question_id):
    participant = get_object_or_404(Participant, id=participant_id)
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        answer = request.POST.get('answer')
        Answer.objects.create(participant=participant, question=question, answer_text=answer, presentation=question.presentation)
        new_page = question.page + 1
        new_question = Question.objects.filter(presentation=question.presentation, page=new_page).first()
        if new_question:
            return redirect('classroom_quest', participant_id=participant.id, question_id=new_question.id)
        else:
            return redirect('karne', participant_id=participant.id, presentation_id=question.presentation.id)

    context={
        'question' : question
    }
    return render(request, "soru.html", context)

def karne(request, participant_id, presentation_id):
    participant = get_object_or_404(Participant, id=participant_id)
    presentation = get_object_or_404(Presentation, id=presentation_id)
    answers = Answer.objects.filter(participant=participant, presentation=presentation)
    context={
        'answers': answers,
        'participant': participant,
        'presentation': presentation,
    }
    return render(request, "karne.html", context)



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Form alanlarının boş olmaması kontrolü
        if not username or not password:
            messages.error(request, "Kullanıcı adı ve şifre alanları doldurulmalıdır.")
            return render(request, 'login.html', {'show_navbar': False})
        
        # Kullanıcı doğrulama
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('presentation_lists'))  # 'base' adlı bir URL'nin tanımlı olduğundan emin olun
        else:
            messages.error(request, "Kullanıcı adı veya şifre yanlış.")
    
    return render(request, 'login.html', {'show_navbar': False})

def logout_view(request):
    logout(request)
    return redirect('login')


def create_company(request):
      form = CompanyForm()
      if request.method == "POST":
            form = CompanyForm(request.POST, request.FILES)
            if form.is_valid():
                  new_object = form.save()
                  return redirect('company_lists')
      return render(request, 'company-create.html', {'show_navbar': True, 'title': "Şirket Oluştur", 'form': form})

def company_lists(request):
     companies = Company.objects.all().order_by('-is_active')

     return render(request, 'company-list.html', {'show_navbar': True, 'title': "Şirket Listesi", 'companies': companies})

from django.shortcuts import get_object_or_404

def update_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    form = CompanyForm(instance=company)

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_lists')

    return render(request, 'company-create.html', {'show_navbar': True, 'title': "Şirket Güncelle", 'form': form, 'company': company})


def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":
        company.is_active = False
        company.save()
        return HttpResponseRedirect(reverse('company_lists'))

    return render(request, 'company-list.html', {'show_navbar': True, 'title': "Şirket Sil", 'company': company})

def reload_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "POST":
        company.is_active = True
        company.save()
        return HttpResponseRedirect(reverse('company_lists'))

    return render(request, 'company-list.html', {'show_navbar': True, 'title': "Şirket Geri Yükle", 'company': company})




def presentation_create(request):
      form = PresentationForm()
      if request.method == "POST":
            form = PresentationForm(request.POST, request.FILES)
            if form.is_valid():
                  new_object = form.save()
                  return redirect('presentation_lists')
      return render(request, 'company-create.html', {'show_navbar': True, 'title': "Sunum Oluştur", 'form': form})


def presentation_lists(request):
     presentations = Presentation.objects.all().order_by('-is_active')

     return render(request, 'company-list.html', {'show_navbar': True, 'title': "Sunum Listesi", 'presentations': presentations})


def update_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    form = PresentationForm(instance=presentation)

    if request.method == "POST":
        form = PresentationForm(request.POST, request.FILES, instance=presentation)
        if form.is_valid():
            form.save()
            return redirect('presentation_lists')

    return render(request, 'company-create.html', {'show_navbar': True, 'title': "Şirket Güncelle", 'form': form, 'company': presentation})


def delete_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)

    if request.method == "POST":
        presentation.is_active = False
        presentation.save()
        return HttpResponseRedirect(reverse('presentation_lists'))

    return render(request, 'company-list.html', {'show_navbar': True, 'title': "Şirket Sil", 'company': presentation})

def reload_presentation(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)

    if request.method == "POST":
        presentation.is_active = True
        presentation.save()
        return HttpResponseRedirect(reverse('presentation_lists'))

    return render(request, 'company-list.html', {'show_navbar': True, 'title': "Şirket Geri Yükle", 'company': presentation})



def question_create(request, presentation_id):
    presentation = get_object_or_404(Presentation, id=presentation_id)
    questions = Question.objects.filter(presentation=presentation).order_by("-is_active")
    
    # Form oluştururken presentation'ı aktar
    form = QuestionForm(presentation=presentation)
    
    if request.method == "POST":
        form = QuestionForm(request.POST, presentation=presentation)
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.presentation = presentation
            new_object.save()
            return redirect('presentation_lists')
    
    return render(
        request, 
        'components/create_form.html', 
        {
            'show_navbar': True,
            'presentation_id': presentation_id,
            'questions': questions,
            'title2': f"{presentation.company} şirketinin {presentation.name} sunumu için Soru Listesi",
            'title': f"{presentation.company} şirketinin {presentation.name} sunumu için Soru Oluştur",
            'form': form
        }
    )

def question_lists(request):
    questions = Question.objects.all().order_by('-is_active')

    return render(request, 'question-list.html', {'show_navbar': True, 'title': "Soru Listesi", 'questions': questions})


def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    form = PresentationForm(instance=question)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_lists')

    return render(request, 'company-create.html', {'show_navbar': True, 'title': "Soru Güncelle", 'form': form, 'company': question})


def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        question.is_active = False
        question.save()
        return HttpResponseRedirect(reverse('question_lists'))

    return render(request, 'question-list.html', {'show_navbar': True, 'title': "Soru Sil", 'company': question})

def reload_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        question.is_active = True
        question.save()
        return HttpResponseRedirect(reverse('question_lists'))

    return render(request, 'question-list.html', {'show_navbar': True, 'title': "Soru Geri Yükle", 'company': question})

def select_presentation(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    sunumlar = Presentation.objects.filter(company=company, is_active=True)
    return render(request, 'components/sinif/sunum_sec.html', {'sunumlar': sunumlar, 'company': company})


import random
import string
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def create_classroom_company(request):
    companies = Company.objects.filter(is_active=True)

    return render(request, 'classroom-company-list.html', {'show_navbar': True, 'title': "Sınıf İçin Şirket Listesi", 'companies': companies})

def generate_random_code(length=8):
    """ Rastgele sınıf kodu oluşturur. """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def create_classroom(request, company_id, presentation_id):
    """ Rastgele bir kod ve QR ile sınıf oluşturur. """
    company = get_object_or_404(Company, id=company_id)
    presentation = get_object_or_404(Presentation, id=presentation_id)

    # Rastgele bir kod oluştur
    random_code = generate_random_code()

    # QR kodunu oluştur
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    url = f"http://127.0.0.1:8000/classroom/join/{random_code}/{presentation.id}/"
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_image = ContentFile(buffer.getvalue(), name=f"{random_code}.png")

    classroom = Classroom.objects.create(
        company=company,
        code=random_code,
        qr_image=qr_image
    )
    return redirect('base', classroom_id=classroom.id, presentation_id=presentation.id)
