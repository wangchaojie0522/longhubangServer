
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from django.urls import re_path , include
import myApp.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(myApp.urls)),
    path(r'', TemplateView.as_view(template_name='index.html'))
]
