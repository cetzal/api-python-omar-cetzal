from django.urls import path
from .views import LoginView, LogoutView, CustomTokenRefreshView

urlpatterns = [
    path('signin/', LoginView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
