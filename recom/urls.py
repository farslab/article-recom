from django.urls import path
from . import views
from django.shortcuts import redirect

def custom_login_redirect(request):
    return redirect('/login')
urlpatterns = [
    path("", views.recommended_articles, name='index'),
    path("", views.recommended_articles, name='recommended_articles'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/login/', custom_login_redirect),

]
