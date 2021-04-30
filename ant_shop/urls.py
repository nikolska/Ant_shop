"""ant_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from products.views import CategoryCreateView, CategoryView, CategoryListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CategoryListView.as_view(), name='category_list'),
    re_path(r'^categories/(?P<pk>\d+)/$', CategoryView.as_view(), name='category'),
    path('categories/add/', CategoryCreateView.as_view(), name='create_category'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
