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

    path('dashboard/index/',admin_index_dashboard, name='dashboard_index'),
    path('dashboard/index/edit/<int:id>/', edit_index, name='dashboard_edit_index'),
    path('dashboard/index/delete/<int:id>/', delete_index, name='dashboard_delete_index'),
    path('dashboard/index/bg/delete/<int:id>/', delete_bg_image, name='dashboard_delete_bg_image'),

    path('gallery/delete/<int:id>/', delete_gallery_image, name='delete_gallery_image'),
    path('dashboard/about/', dashboard_about, name='dashboard_about'),
    path('dashboard/about/edit/<int:id>/', edit_about, name='edit_about'),

    path('about/add-attorney/', admin_add_attorney, name='admin_add_attorney'),
    path('dashboard/attorney/edit/<int:id>/', edit_attorney, name='edit_attorney'),
    path('dashboard/attorney/delete/<int:id>/', delete_attorney, name='delete_attorney'),



    path('portfolio/', admin_portfolio, name='admin_portfolio'),
    path('portfolio/main/edit/<int:id>/', admin_edit_portfolio_main, name='admin_edit_portfolio_main'),


    path('portfolio/client/edit/<int:id>/', admin_edit_client, name='admin_edit_client'),
    path('portfolio/client/delete/<int:id>/', admin_delete_client, name='admin_delete_client'),
    path('portfolio/client/add/', admin_add_client, name='admin_add_client'),
    path('portfolio/item/add/', admin_add_portfolio_item, name='admin_add_portfolio_item'),
    path('portfolio/item/edit/<int:id>/', admin_edit_portfolio_item, name='admin_edit_portfolio_item'),
    path('portfolio/item/delete/<int:id>/', admin_delete_portfolio_item, name='admin_delete_portfolio_item'),


    path('blog/', admin_blog_dashboard, name='admin_blog_dashboard'),

    path('blog/edit/<int:id>/', admin_edit_blog_main, name='admin_edit_blog_main'),

    path('blog/post/add/', admin_add_blog_post, name='admin_add_blog_post'),
    path('blog/post/edit/<int:id>/', admin_edit_blog_post, name='admin_edit_blog_post'),
    path('blog/post/delete/<int:id>/', admin_delete_blog_post, name='admin_delete_blog_post'),


    path('blog/comment/delete/<int:id>/', admin_delete_comment, name='admin_delete_comment'),

    path('blog/author/add/', admin_add_author, name='admin_add_author'),
    path('blog/author/edit/<int:id>/', admin_edit_author, name='admin_edit_author'),
    path('blog/author/delete/<int:id>/', admin_delete_author, name='admin_delete_author'),

    path('practice-area/', dashboard_practice_area, name='dashboard_practice_area'),
    path('practice-area/add/', add_service, name='add_service'),
    path('practice-area/edit/<int:id>/', edit_service, name='edit_service'),
    path('practice-area/delete/<int:id>/', delete_service, name='delete_service'),

    path('legal-advice/', dashboard_legal_advice, name='dashboard_legal_advice'),
    path('legal-advice/delete/<int:pk>/', delete_legal_advice, name='delete_legal_advice'),

    path('dashboard/organization-settings/', admin_organization_settings, name='admin_organization_settings'),
    path('dashboard/attorneys/', dashboard_attorneys, name='dashboard_attorneys'),
    path('dashboard/clients/', admin_clients_dashboard, name='dashboard_clients'),










]
