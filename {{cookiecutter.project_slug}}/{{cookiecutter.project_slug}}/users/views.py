from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from {{cookiecutter.project_slug}}.docs.serializers.doc_serializers import MessageSerializer
from {{cookiecutter.project_slug}}.permissions import permissions
from {{cookiecutter.project_slug}}.utils import JWT_token, bucket
from . import serializers
from .docs import doc_serializers
from .models import User
from .tasks import send_verification_email


class UsersListAPI(ListAPIView):
    """
    Returns list of users.\n
    allowed methods: GET.
    """
    permission_classes = [IsAdminUser, ]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filterset_fields = ['last_login', 'is_active', 'is_admin', 'is_superuser']
    search_fields = ['username', 'email']


class UserRegisterAPI(CreateAPIView):
    """
    Registers a User.\n
    allowed methods: POST.
    """
    model = User
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [permissions.NotAuthenticated, ]

    @extend_schema(responses={201: doc_serializers.DocRegisterSerializer})
    def post(self, request, *args, **kwargs):
        srz_data = self.serializer_class(data=request.POST)
        if srz_data.is_valid():
            srz_data.validated_data.pop('password2')
            user = User.objects.create_user(**srz_data.validated_data)
            vd = srz_data.validated_data
            send_verification_email.delay_on_commit(vd['email'], user.id)
            response = srz_data.data
            response['message'] = 'we sent you an activation url.'
            return Response(
                data={'data': response},
                status=status.HTTP_200_OK,
            )
        return Response(
            data={'error': srz_data.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserRegisterVerifyAPI(APIView):
    """
    Verification view for registration.\n
    allowed methods: GET.
    """
    permission_classes = [permissions.NotAuthenticated, ]
    http_method_names = ['get']
    serializer_class = doc_serializers.DocRegisterVerifySerializer

    def get(self, request, token):
        token_result = JWT_token.get_user(token)
        if not isinstance(token_result, User):
            return token_result
        if token_result.is_active:
            return Response(data={'message': 'this account already is active'}, status=status.HTTP_400_BAD_REQUEST)
        token_result.is_active = True
        token_result.save()
        token = JWT_token.generate_token(token_result)
        return Response(data={
            'message': 'Account activated successfully',
            'token': token['token'],
            'refresh': token['refresh']},
            status=status.HTTP_200_OK
        )


class ResendVerificationEmailAPI(APIView):
    """
    makes a new token and sends it with email.\n
    allowed methods: POST.
    """
    permission_classes = [permissions.NotAuthenticated, ]
    serializer_class = serializers.ResendVerificationEmailSerializer

    @extend_schema(responses={200: MessageSerializer})
    def post(self, request):
        srz_data = self.serializer_class(data=request.POST)
        if srz_data.is_valid():
            user = srz_data.validated_data['user']
            send_verification_email.delay_on_commit(user.email, user.id)
            return Response(
                data={"message": "The activation email has been sent again successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(data={'errors': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPI(APIView):
    """
    Changes a user password.\n
    allowed methods: POST.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.ChangePasswordSerializer

    @extend_schema(responses={
        200: MessageSerializer
    })
    def put(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            user = request.user
            old_password = srz_data.validated_data['old_password']
            new_password = srz_data.validated_data['new_password']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response(data={'message': 'Your password changed successfully!'}, status=status.HTTP_200_OK)
            return Response(data={'error': 'Your old password is not correct'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class SetPasswordAPI(APIView):
    """
    set user password for reset_password.\n
    allowed methods: POST.
    """
    permission_classes = [AllowAny, ]
    serializer_class = serializers.SetPasswordSerializer

    @extend_schema(responses={
        200: MessageSerializer
    })
    def post(self, request, token):
        srz_data = self.serializer_class(data=request.POST)
        token_result = JWT_token.get_user(token)
        if not isinstance(token_result, User):
            return token_result
        if srz_data.is_valid():
            new_password = srz_data.validated_data['new_password']
            token_result.set_password(new_password)
            token_result.save()
            return Response(data={'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPI(APIView):
    """
    reset user passwrd.\n
    allowed methods: POST.
    """
    permission_classes = [AllowAny, ]
    serializer_class = serializers.ResetPasswordSerializer

    @extend_schema(responses={
        200: MessageSerializer
    })
    def post(self, request):
        srz_data = self.serializer_class(data=request.POST)
        if srz_data.is_valid():
            try:
                user = get_object_or_404(User, email=srz_data.validated_data['email'])
            except Http404:
                return Response(data={'error': 'user with this Email not found!'}, status=status.HTTP_400_BAD_REQUEST)
            send_verification_email.delay_on_commit(user.email, user.id)
            return Response(data={'message': 'sent you a change password link!'}, status=status.HTTP_200_OK)
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class BlockTokenAPI(APIView):
    """
    blocks a deleted token\n
    allowed methods: POST.
    """
    serializer_class = serializers.TokenSerializer
    permission_classes = [AllowAny, ]

    @extend_schema(responses={200: MessageSerializer})
    def post(self, request):
        srz_data = self.serializer_class(data=request.POST)
        if srz_data.is_valid():
            try:
                token = RefreshToken(request.POST['refresh'])
            except TokenError:
                return Response(data={'error': 'token is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
            token.blacklist()
            return Response(data={'message': 'Token blocked successfully!'}, status=status.HTTP_200_OK)
        return Response(data={'error': srz_data.errors}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    patch=extend_schema(
        responses={200: MessageSerializer}
    ),
    delete=extend_schema(
        responses={200: MessageSerializer}
    )
)
class UserProfileAPI(RetrieveUpdateDestroyAPIView):
    """
    Retrieve or update user profile.\n
    allowed methods: GET, PATCH, DELETE.\n
    GET: Retrieve, PATCH:partial update, DELETE: delete account.
    """
    permission_classes = [permissions.IsOwnerOrReadOnly]
    serializer_class = serializers.UserSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
    queryset = User.objects.filter(is_active=True)
    http_method_names = ['get', 'patch', 'delete']

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            email_changed = 'email' in serializer.validated_data
            message = 'Updated profile successfully.'
            if email_changed:
                user.is_active = False
                user.save()
                send_verification_email.delay_on_commit(serializer.validated_data['email'], user.id)
                message += ' A verification URL has been sent to your new email address.'

            serializer.save()

            return Response(data={'message': message}, status=status.HTTP_200_OK)
        return Response(data={'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        bucket.bucket.delete_object(self.get_object().profile.avatar.name)
        response = super().destroy(request, *args, **kwargs)
        if response.status_code != 204:
            return response
        return Response(data={'message': 'your account deleted successfully.'})
