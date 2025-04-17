from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('new/', views.recipe_create, name='recipe_create'),
    path('<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('<int:pk>/rate/', views.add_rating, name='add_rating'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('recipes/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
]