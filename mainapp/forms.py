from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
import json


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        label="E-posta", 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Kullanıcı Adı',
            'password1': 'Şifre',
            'password2': 'Şifre (Tekrar)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Kullanıcı Adı',
            'email': 'E-posta',
            'first_name': 'Ad',
            'last_name': 'Soyad',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Kullanıcı Adı", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Şifre", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )



class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo']  # Güncellenebilir alanlar
        labels = {
            'name': 'Şirket Adı',
            'logo': 'Logo',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'


class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['name', 'bg_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adı giriniz'}),
            'bg_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Adı',
            'bg_image': 'Arka Plan Görseli',
        }

class QuestionForm(forms.Form):
    question_number = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Soru numarasını giriniz'}),
        label="Soru Numarası"
    )
    question_text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Soruyu giriniz'}),
        label="Soru Metni"
    )

    def save_to_json(self, existing_questions):
        """
        Mevcut sorular JSON'ını alır, yeni bir soru ekler.
        :param existing_questions: Mevcut JSON verisi (dict olarak)
        :return: Güncellenmiş JSON verisi
        """
        if not isinstance(existing_questions, list):
            existing_questions = []

        # Yeni soruyu ekle
        question_number = self.cleaned_data['question_number']
        question_text = self.cleaned_data['question_text']

        new_question = {
            "question_number": question_number,
            "question_text": question_text
        }

        existing_questions.append(new_question)

        # Güncellenmiş JSON'u döndür
        return json.dumps(existing_questions)



class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["name", "email", "office"]
        labels = {
            "name": "Adı",
            "email": "E-posta",
            "office": "Ofis",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Adınızı girin"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-posta adresinizi girin"}),
            "office": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ofis bilgisi"}),
        }