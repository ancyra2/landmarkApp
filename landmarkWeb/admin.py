from django.contrib import admin
from .models import ImageModel, landmarkModel
# Register your models here.

admin.site.register(ImageModel)
admin.site.register(landmarkModel)