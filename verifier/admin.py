from django.contrib import admin

# Register your models here.
from .models import Institution, DocumentBlockModel


admin.site.register(Institution)
admin.site.register(DocumentBlockModel)