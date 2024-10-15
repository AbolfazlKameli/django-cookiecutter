from django.urls import reverse, resolve
from rest_framework.test import APISimpleTestCase
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users import views


class TestUrls(APISimpleTestCase):
    # Tokens
    def test_token_obtain_pair_url(self):
        token_obtain_pair_url = reverse('users:token-obtain-pair')
        self.assertEqual(resolve(token_obtain_pair_url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url(self):
        token_refresh_url = reverse('users:token-refresh')
        self.assertEqual(resolve(token_refresh_url).func.view_class, TokenRefreshView)

    def test_token_block_url(self):
        token_block_url = reverse('users:token-block')
        self.assertEqual(resolve(token_block_url).func.view_class, views.BlockTokenAPI)

    # Password
    def test_change_password_url(self):
        password_change_url = reverse('users:change-password')
        self.assertEqual(resolve(password_change_url).func.view_class, views.ChangePasswordAPI)

    def test_reset_password_url(self):
        password_reset_url = reverse('users:reset-password')
        self.assertEqual(resolve(password_reset_url).func.view_class, views.ResetPasswordAPI)

    def test_set_password_url(self):
        set_password_url = reverse('users:set-password', args=('this is a test token',))
        self.assertEqual(resolve(set_password_url).func.view_class, views.SetPasswordAPI)

    # Registration
    def test_user_register_url(self):
        user_register_url = reverse('users:user-register')
        self.assertEqual(resolve(user_register_url).func.view_class, views.UserRegisterAPI)

    def test_register_verify_url(self):
        register_verify_url = reverse('users:user-register-verify', args=('this is a test token',))
        self.assertEqual(resolve(register_verify_url).func.view_class, views.UserRegisterVerifyAPI)

    def test_resend_verification_email_url(self):
        resend_verification_url = reverse('users:user-register-resend-email')
        self.assertEqual(resolve(resend_verification_url).func.view_class, views.ResendVerificationEmailAPI)

    # User Info
    def test_user_profile_url(self):
        user_profile_url = reverse('users:user-profile', args=(21,))
        self.assertEqual(resolve(user_profile_url).func.view_class, views.UserProfileAPI)

    def test_user_list_url(self):
        user_list_url = reverse('users:users-list')
        self.assertEqual(resolve(user_list_url).func.view_class, views.UsersListAPI)
