from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from users.models import Role
from rest_framework.response import Response


class IsCreatorPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == Role.CREATOR_ROLE


class IsUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == Role.USER_ROLE


class CreatorOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsCreatorPermission]

    def get(self, request):
        return Response("Hello, creator!")

    def post(self, request):
        return Response("Creator, you can post!")

    def put(self, request):
        return Response("Creator, you can put!")


class UserOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsUserPermission]

    def get(self, request):
        return Response("Hello, user!")

    def post(self, request):
        return Response("User, you can post!")

    def put(self, request):
        return Response("User, you can put!")