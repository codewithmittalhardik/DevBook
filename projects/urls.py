from django.urls import path
from . import views

urlpatterns = [
    # Global Landing Page
    path('', views.dashboard, name='dashboard'),
    
    # Global Projects Registry
    path('projects/', views.projects_list, name='projects_list'),
    
    # About Project Page
    path('about/', views.about_project, name='about_project'),
    
    # User Authentication Paths
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Developer Profile Path
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/delete/', views.profile_delete, name='profile_delete'),
    
    # Project CRUD Paths
    path('project/add/', views.project_create, name='project_create'),
    path('project/<int:pk>/edit/', views.project_update, name='project_update'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('project/<int:pk>/reviews/', views.project_reviews, name='project_reviews'),
]