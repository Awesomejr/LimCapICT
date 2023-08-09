from django.urls import path, include
from . import views

app_name = "base"
urlpatterns = [
    path("", views.index, name="home"),
    path("register/", views.registerPage, name="registrationPage"),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path("accounts/login/", views.loginPage, name="loginPage"),
    path("logout/", views.logoutUser, name="logout"),
    # path("profile/<str:pk>/", views.profilePage, name="profilePage"),
    # path("updateProfile/<str:pk>/", views.updateProfile, name="updateProfile"),
    path("about/", views.aboutPage, name="aboutPage"),

    path('profile/edit/<str:pk>/', views.profilePage, name='profilePage'),
]
