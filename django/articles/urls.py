from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list_create, name='article_list_create'),
    path('<int:article_pk>/', views.article_detail_update_delete, name='article_detail_update_delete'),
    path('comments/', views.comment_list, name='comment_list'),
    path('comments/<int:comment_pk>/', views.comment_detail, name='comment_detail'),
]
