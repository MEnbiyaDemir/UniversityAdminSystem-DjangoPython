
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length = 50,verbose_name = "Başlık")
    completed = models.BooleanField(verbose_name = "Durum")

    def __str__(self):
        return self.title


class Pdf(models.Model):
    studentname=models.CharField(max_length=50,verbose_name='Öğrenci Adı')
    studentno=models.CharField(max_length=50,verbose_name='Öğrenci Numarası')
    studenttype=models.CharField(max_length=50,verbose_name='Öğretim Türü')
    projecttype=models.CharField(max_length=50,verbose_name='Ders Adı')
    projectsummary=models.TextField(verbose_name='Proje Özeti')
    projectdate=models.CharField(max_length=50,verbose_name='Teslim Edildiği Dönem')
    projecttitle=models.CharField(max_length=100,verbose_name='Proje Başlığı')
    keywords=models.TextField(max_length=200,verbose_name='Anahtar Kelimeler')
    counselorname=models.CharField(max_length=50,verbose_name='Danışman Adı')
    counselordegree=models.CharField(max_length=50,verbose_name='Danışman Ünvan')
    juryname=models.CharField(max_length=50,verbose_name='Jüri Adı')
    jurydegree=models.CharField(max_length=50,verbose_name='Jüri Ünvan')
    pdfself=models.FileField(verbose_name='Pdf Dosyası')

    