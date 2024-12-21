from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class Trainer(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="trainer_profile",
        verbose_name="Kullanıcı"
    )
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        verbose_name="Telefon"
    )
    photo = models.ImageField(
        upload_to="trainer_photos/", 
        blank=True, 
        null=True, 
        verbose_name="Fotoğraf"
    )
    about = RichTextField(verbose_name="Hakkında")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    def __str__(self):
        return self.user.username


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Adı")
    logo = models.ImageField(
        upload_to="company_logos/", 
        blank=True, 
        null=True, 
        verbose_name="Logo"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    def __str__(self):
        return self.name


class Classroom(models.Model):
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name="classrooms", 
        verbose_name="Şirket"
    )
    code = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Kod"
    )
    qr_image = models.ImageField(
        upload_to="qr_codes/", 
        blank=True, 
        null=True, 
        verbose_name="QR Kod"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    def __str__(self):
        return self.code


class Presentation(models.Model):
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name="presentations", 
        verbose_name="Şirket"
    )
    name = models.CharField(max_length=255, verbose_name="Adı")
    bg_image = models.ImageField(
        upload_to="presentation_bg/", 
        blank=True, 
        null=True, 
        verbose_name="Arka Plan Görseli"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    def __str__(self):
        return self.name


class Question(models.Model):
    presentation = models.ForeignKey(
        Presentation, 
        on_delete=models.CASCADE, 
        related_name="questions", 
        verbose_name="Sunum"
    )
    page = models.IntegerField(verbose_name="Sayfa")
    question_text = models.TextField(verbose_name="Soru")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    def __str__(self):
        return f"{self.presentation.name} - Sayfa {self.page}"


class Participant(models.Model):
    name = models.CharField(max_length=255, verbose_name="Adı")
    email = models.EmailField(unique=True, verbose_name="E-posta")
    company = models.ForeignKey(
        Company, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="participants", 
        verbose_name="Şirket"
    )
    branch = models.CharField(max_length=255, blank=True, null=True, verbose_name="Şube")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    def __str__(self):
        return self.name


class Answer(models.Model):
    participant = models.ForeignKey(
        Participant, 
        on_delete=models.CASCADE, 
        related_name="answers", 
        verbose_name="Katılımcı"
    )
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name="answers", 
        verbose_name="Soru"
    )
    presentation = models.ForeignKey(
        Presentation, 
        on_delete=models.CASCADE, 
        related_name="answers", 
        verbose_name="Sunum",
        blank=True,
        null=True
    )
    answer_text = models.TextField(verbose_name="Cevap")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif Mi?")

    def __str__(self):
        return f"{self.participant.name} - {self.question.question_text[:30]}"
