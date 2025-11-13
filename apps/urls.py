from django.contrib import admin
from django.urls import path
from django.urls import include
from apps.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',index, name='index'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('gallery/',gallery, name='gallery'),
    path('main/',main, name='main'),
    path('practice/',practice, name='practice'),
    path('practice/<int:id>/', practice_area_detail, name='practice-area-detail'),
    path('portfolio/',portfolio, name='portfolio'),
    path('blog/',blog_main, name='blog_main'),
    path('blog/<int:id>/', blog_single, name='blog_single'),
    path('portfolio/<int:id>/', portfolio_detail, name='portfolio-detail'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)