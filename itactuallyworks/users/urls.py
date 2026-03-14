from django.contrib import admin
from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    path('', views.homepage1, name='homepage1'),      # homepage1
    path('signup/', views.signup, name='signup'),     # signup  
    path('login/', views.login_view, name='login'),   # login
    path('forgotpassword/', views.forgotpassword_view, name='forgotpassword'),
    path('homepage/', views.homepage, name='homepage'), # homepage
    path('domainselection/', views.domain, name='domain'),
    path('projects/', views.projects, name='projects'),
    path('projectdetail/', views.projectdetail, name='projectdetail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bookmark/<int:project_id>/', views.bookmark_project, name='bookmark'),
    path('bookmarks/', views.bookmark_page, name='bookmark_page'),
    path('feedback/',views.feedback , name='feedback'),
    path('logout/', views.logout_view, name='logout'),  # logout
    path('chatbot/', views.chatbot, name='chatbot'),
]


