from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .models import User as CustomUser
from notifications.utils import create_notification


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": UserSerializer(user, context={"request": request}).data,
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": UserSerializer(user, context={"request": request}).data,
                    "token": token.key,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class FollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.following.add(target_user)
        try:
            create_notification(
                recipient=target_user,
                actor=request.user,
                verb="followed you",
                target=None,
            )
        except Exception:
            pass
        return Response(
            {"detail": f"Now following {target_user.username}."},
            status=status.HTTP_200_OK,
        )


class UnfollowUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.following.remove(target_user)
        return Response(
            {"detail": f"Unfollowed {target_user.username}."},
            status=status.HTTP_200_OK,
        )


class FollowersListView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        data = UserSerializer(
            user.followers.all(), many=True, context={"request": request}
        ).data
        return Response({"count": len(data), "results": data}, status=status.HTTP_200_OK)


class FollowingListView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        data = UserSerializer(
            user.following.all(), many=True, context={"request": request}
        ).data
        return Response({"count": len(data), "results": data}, status=status.HTTP_200_OK)
