from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register((ClassRoom,ClassStudents,Chat))
admin.site.register((ClassTest,MCQuestion))
admin.site.register((StudentTestResponse,MCQStudentResponse))