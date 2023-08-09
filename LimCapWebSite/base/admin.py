from django.contrib import admin
from .models import User, Message, Course, StudyGroup

# Register your models here.
admin.site.register(User)
admin.site.register(Message)
admin.site.register(Course)
admin.site.register(StudyGroup)
