from django.contrib import admin

from .models import *

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(User_Response)
admin.site.register(EasyQuestion)