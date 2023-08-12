from django.urls import path, include
from . import views

app_name = "base"
urlpatterns = [
    path("", views.index, name="home"),
    path("register/", views.registerPage, name="registrationPage"),
    path("accounts/login/", views.loginPage, name="loginPage"),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('profile/edit/<str:pk>/', views.profilePage, name='profilePage'),
    path('CoursePurchase/<str:pk>/', views.purchaseCourse, name='purchaseCourse'),
    path("confirmPayment/<str:pk>/", views.confirmPayment, name="confirmPayment"),
    path("about/", views.aboutPage, name="aboutPage"),
    path("logout/", views.logoutUser, name="logout"),
]
