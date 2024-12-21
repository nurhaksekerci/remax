from django import forms
from .models import Company, Presentation, Question, Participant

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo']
        labels = {
            'name': 'Şirket Adı',
            'logo': 'Şirket Logosu',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Şirket adını giriniz'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# Presentation ModelForm
class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['company', 'name', 'bg_image']
        labels = {
            'company': 'Şirket',
            'name': 'Sunum Adı',
            'bg_image': 'Arka Plan Görseli',
        }
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sunum adını giriniz'}),
            'bg_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # company alanını filtrele
        self.fields['company'].queryset = Company.objects.filter(is_active=True)

# Question ModelForm
from django.db.models import Max  # Gerekli import

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['page', 'question_text']
        labels = {
            'page': 'Sayfa Numarası',
            'question_text': 'Soru Metni',
        }
        widgets = {
            'page': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sayfa numarasını giriniz'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Soruyu giriniz'}),
        }

    def __init__(self, *args, **kwargs):
        presentation = kwargs.pop('presentation', None)
        super().__init__(*args, **kwargs)

        # Sunuma ait en yüksek page değerini bul
        if presentation:
            max_page = Question.objects.filter(presentation=presentation).aggregate(Max('page'))['page__max']
            self.fields['page'].initial = (max_page + 1) if max_page is not None else 1

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'branch']
        labels = {
            'name': 'Ad Soyad',
            'email': 'E-posta',
            'branch': 'Şube',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınızı giriniz'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta adresinizi giriniz'}),
            'branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Şube adını giriniz'}),
        }
