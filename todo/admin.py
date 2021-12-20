from django.contrib import admin
from .models import Todo
from .models import Pdf

# Register your models here.

admin.site.register(Todo)

@admin.register(Pdf)
class VenueAdmin(admin.ModelAdmin):
    list_display=('studentname','studentno','studenttype','projecttype',
    'projectdate','projecttitle','keywords','counselorname','counselordegree','juryname','jurydegree','pdfself')
    ordering=('studentname',)
    search_fields = ('studentname','studentno','projecttitle','keywords','pdfself')
    list_filter=('studenttype','projecttype','projectdate','counselorname','juryname')