from django.contrib.auth import get_user_model
from .models import ShippingAddress
from .serializers import (
    PasswordChangeSerializer, 
    PasswordResetConfirmSerializer,
    VerifyEmailSerializer, 
    UserSerializer, 
    ShippingAddressSerializer
    )
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (GenericAPIView,
    ListAPIView,
    CreateAPIView, 
    RetrieveUpdateAPIView, 
    RetrieveUpdateDestroyAPIView
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotAcceptable
from user.permissions import IsUserOwner
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from allauth.account.views import ConfirmEmailView
from rest_auth.registration.views import RegisterView
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from .send_mail import send_register_mail, send_reset_password_email

UserModel = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

class DeleteA(APIView):
    def get(self, request, *args, **kwargs):
        try:
            print(UserModel.objects.get(username=request.data['username']))
            UserModel.objects.get(username=request.data['username']).delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        response = Response({"detail": _("Successfully logged out.")},
                            status=status.HTTP_200_OK)
        return response

class RegisterAPIView(RegisterView):
    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterAPIView, self).dispatch(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            self.get_response_data(user),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        email = EmailAddress.objects.get(email=user.email, user=user)
        confirmation = EmailConfirmationHMAC(email)
        key = confirmation.key
        send_register_mail(self, user, key)
        return user


class VerifyEmailView(APIView, ConfirmEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)


class PasswordChangeView(GenericAPIView):
    """
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been saved.")})


class PasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise NotAcceptable(_("Please enter a valid email."))
        send_reset_password_email(self, user)
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Password has been reset with the new password.")})


class ProfileView(RetrieveUpdateAPIView):

    queryset = UserModel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class AddressViewSet(ModelViewSet):

    queryset = ShippingAddress.objects.all()
    permission_classes = (IsUserOwner,)
    serializer_class = ShippingAddressSerializer
    
    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(user=user)


class AddressView(ListAPIView):

    queryset = ShippingAddress.objects.all()
    permission_classes = (IsUserOwner,)
    serializer_class = ShippingAddressSerializer

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(user=user)


class AddressDetailView(RetrieveUpdateDestroyAPIView):

    queryset = ShippingAddress.objects.all()
    permission_classes = (IsUserOwner,)
    serializer_class = ShippingAddressSerializer


class CreateAddressView(CreateAPIView):

    queryset = ShippingAddress.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ShippingAddressSerializer

  

