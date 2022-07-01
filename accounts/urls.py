

from django.urls import path

from .views import (
    RegisterView,
    UserLoginView,
    ChangePasswordView
)

app_name = 'accounts'
urlpatterns = [
    path('register', RegisterView.as_view(),),
    path('login', UserLoginView.as_view(),),
    path('change-password', ChangePasswordView.as_view(),)

    
]


