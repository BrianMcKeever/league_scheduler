from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path(r'', TemplateView.as_view(template_name="portal.html"), name = "portal"),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
]

