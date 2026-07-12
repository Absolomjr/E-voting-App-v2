from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.permissions import IsMemberManager, IsSuperAdmin
from accounts.serializers import (
    ChangePasswordSerializer,
    MemberCreateSerializer,
    MemberListSerializer,
    MemberLoginSerializer,
    MemberRegistrationSerializer,
    StaffCreateSerializer,
    StaffListSerializer,
    StaffLoginSerializer,
)
from accounts.services import (
    AuthenticationService,
    MemberManagementService,
    MemberRegistrationService,
    StaffManagementService,
)

User = get_user_model()


def _staff_payload(user):
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.get_full_name(),
        "email": user.email,
        "role": user.role,
        "is_verified": user.is_verified,
    }


def _member_payload(user):
    profile = user.member_profile
    return {
        "id": user.id,
        "full_name": user.get_full_name(),
        "email": user.email,
        "role": user.role,
        "member_number": profile.member_number,
        "phone": profile.phone,
        "is_verified": user.is_verified,
    }


class StaffLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StaffLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, error = AuthenticationService().authenticate_staff(
            serializer.validated_data["username"],
            serializer.validated_data["password"],
        )
        if error:
            return Response({"detail": error}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": _staff_payload(user),
        })


class MemberLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MemberLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, error = AuthenticationService().authenticate_member(
            serializer.validated_data["member_number"],
            serializer.validated_data["password"],
        )
        if error:
            return Response({"detail": error}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": _member_payload(user),
        })


class MemberRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MemberRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = MemberRegistrationService().register(serializer.validated_data)
        return Response(
            {
                "detail": "Registration submitted. Await verification by the SACCO.",
                "member_number": profile.member_number,
            },
            status=status.HTTP_201_CREATED,
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_member_user:
            return Response(_member_payload(user))
        return Response(_staff_payload(user))


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data["current_password"]):
            return Response(
                {"detail": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Password updated."})


class MemberListCreateView(APIView):
    permission_classes = [IsMemberManager]

    def get(self, request):
        qs = MemberManagementService().list_members(request.query_params)
        return Response(MemberListSerializer(qs, many=True).data)

    def post(self, request):
        serializer = MemberCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = MemberRegistrationService().register(
            serializer.validated_data,
            auto_verify=True,
        )
        return Response(
            MemberListSerializer(profile.user).data,
            status=status.HTTP_201_CREATED,
        )


class MemberVerifyView(APIView):
    permission_classes = [IsMemberManager]

    def post(self, request, member_id):
        user = MemberManagementService().verify(member_id, request.user)
        return Response(MemberListSerializer(user).data)


class MemberDeactivateView(APIView):
    permission_classes = [IsMemberManager]

    def post(self, request, member_id):
        user = MemberManagementService().deactivate(member_id, request.user)
        return Response(MemberListSerializer(user).data)


class StaffListCreateView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        qs = StaffManagementService().list_staff()
        return Response(StaffListSerializer(qs, many=True).data)

    def post(self, request):
        serializer = StaffCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = StaffManagementService().create_staff(
            serializer.validated_data,
            request.user,
        )
        return Response(
            StaffListSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class StaffDeactivateView(APIView):
    permission_classes = [IsSuperAdmin]

    def post(self, request, staff_id):
        try:
            user = StaffManagementService().deactivate(staff_id, request.user)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(StaffListSerializer(user).data)
