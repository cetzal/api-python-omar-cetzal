from django.urls import path
from .views import LoginView, LogoutView, CustomTokenRefreshView

urlpatterns = [
    path('signin/', LoginView.as_view(), name='signin'),
]
