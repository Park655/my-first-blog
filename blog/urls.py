from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('supplements_list/', views.supplement_list, name='supplement_list'),
    path('mypage/', views.mypage_view, name='mypage'),
]