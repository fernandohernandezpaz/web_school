"""web_school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from django.conf.urls import url, include
from school.views import PublicViewStudentForParents

urlpatterns = [
    url('jet/', include('jet.urls', 'jet')),
    url('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('admin/', admin.site.urls),
    path('school/', include('school.urls')),
    path('colegio/estudiantes', PublicViewStudentForParents.as_view(), name='public_page')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
