from django.urls import path, re_path
from .views import (
    PasswordResetView,
    PasswordResetConfirmView,
    RegisterAPIView,
    VerifyEmailView, 
    ProfileView, 
    AddressView,
    CreateAddressView,
    AddressDetailView,
)
from rest_auth.views import (
    LoginView,
    PasswordChangeView,
    LogoutView,
)

urlpatterns = [
    # URLs that do not require a session or valid token
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('login/', LoginView.as_view(), name='login'),  
    path('register/', RegisterAPIView.as_view(), name='rest_register'),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
     name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
     name='account_confirm_email'),

    # URLs that require a user to be logged in with a valid session / token.
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/address/', AddressView.as_view(), name='address'),
    path('profile/address/<int:pk>/', AddressDetailView.as_view(), name='address'),
    path('profile/address/create/', CreateAddressView.as_view(), name='create_address'),
]