from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path(r'', TemplateView.as_view(template_name="portal.html"),),
    path('admin/', admin.site.urls),
]

