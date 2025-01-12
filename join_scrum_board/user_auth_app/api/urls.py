"""
URL configuration for join_scrum_board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from user_auth_app.api.views import TokenCheckView, LoginView, SignUpView, PasswordResetView, SetNewPasswordView, GetTimestampView, SetTimestampView, GuestLoginView

urlpatterns = [
    path('token_check/', TokenCheckView.as_view()),
    path('login/', LoginView.as_view()),
    path('guest_login/', GuestLoginView.as_view()),
    path('sign_up/', SignUpView.as_view()),
    path('reset_password/', PasswordResetView.as_view()),
    path('set_new_password/', SetNewPasswordView.as_view()),
    path('get_timestamp/<int:user_id>/', GetTimestampView.as_view()),
    path('set_timestamp/', SetTimestampView.as_view()),
]