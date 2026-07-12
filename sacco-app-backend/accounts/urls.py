from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    ChangePasswordView,
    MemberDeactivateView,
    MemberListCreateView,
    MemberLoginView,
    MemberRegistrationView,
    MemberVerifyView,
    ProfileView,
    StaffDeactivateView,
    StaffListCreateView,
    StaffLoginView,
)

urlpatterns = [
    path("login/staff/", StaffLoginView.as_view()),
    path("login/member/", MemberLoginView.as_view()),
    path("register/", MemberRegistrationView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("password/", ChangePasswordView.as_view()),
    path("members/", MemberListCreateView.as_view()),
    path("members/<int:member_id>/verify/", MemberVerifyView.as_view()),
    path("members/<int:member_id>/deactivate/", MemberDeactivateView.as_view()),
    path("staff/", StaffListCreateView.as_view()),
    path("staff/<int:staff_id>/deactivate/", StaffDeactivateView.as_view()),
]
