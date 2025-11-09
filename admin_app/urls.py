from django.urls import path
from .views import *
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('ad_contact/', ad_contact, name='ad_contact'),
     path('contact/', ad_contact, name='ad_contact'),
    path('contact-info/edit/<int:id>/', edit_contact_info, name='edit_contact_info'),
    path('contact-section/edit/<int:id>/', edit_contact_section, name='edit_contact_section'),
    path('contact-message/delete/<int:id>/', delete_contact_message, name='delete_contact_message'),
    path('gallery/', dashboard_gallery, name='dashboard_gallery'),
    path('gallery/delete/<int:id>/', delete_gallery_image, name='delete_gallery_image'),
    path('admin/about/', about_dashboard, name='about_dashboard'),

    path('admin/about/delete/<int:id>/', admin_delete_about, name='admin_delete_about'),
    path('portfolio/', admin_portfolio, name='admin_portfolio'),
    path('portfolio/main/edit/<int:id>/', admin_edit_portfolio_main, name='admin_edit_portfolio_main'),


    path('portfolio/client/edit/<int:id>/', admin_edit_client, name='admin_edit_client'),
    path('portfolio/client/delete/<int:id>/', admin_delete_client, name='admin_delete_client'),
    path('portfolio/client/add/', admin_add_client, name='admin_add_client'),



]
