from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from .models import User
from .serializers import UserSerializer
from .permissions import IsSuperAdmin, IsAdmin
from .paginations import UserPagination
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .filters import UserFilter



class UserViewSet(ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def get_permissions(self):
        """
        Conditional Permissions Applied:
        - Super Admin: Can perform any action.
        - Admin: Can create, view, and update employees under their supervision.
        """
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsSuperAdmin | IsAdmin]
        elif self.action in ['update', 'partial_update', 'list']:
            self.permission_classes = [IsAdmin | IsSuperAdmin]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        """
        Restricts the queryset based on the user's role.
        - Admins: Can only access employees they supervise.
        - Super Admins: Access to all users.
        """
        user = self.request.user
        
        if user.role == 'admin':
            return User.objects.filter(supervised_by=user)

        return super().get_queryset()

    def perform_create(self, serializer):
        """
        Handles the creation of new users:
        - Admins: Can only create employees.
        - Super Admins: Can create any type of user.
        """
        user = self.request.user
        user_pass = self.request.data.get('password')
        if not user_pass:
            raise PermissionDenied("Password is required.")
        if user.role == 'admin':
            if serializer.validated_data.get('role') not in ['employee']:
                raise PermissionDenied("Admins can only create employees.")
            serializer.save(supervised_by=user, password=make_password(user_pass))
        else:
            serializer.save(password=make_password(user_pass))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        print(request.query_params)
        # Pagination logic start
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            
            return Response(self.get_paginated_response(serializer.data), status=status.HTTP_200_OK)
        # Pagination logic end
        serializer = self.get_serializer(queryset, many=True)
        return Response(self.get_paginated_response(serializer.data), status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Overrides the create method to add a custom response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "User created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Overrides the retrieve method to add a custom response.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "message": "User details retrieved successfully.",
            "data": serializer.data
        },status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """
        Overrides the partial_update method to add a custom response.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            "message": "User updated successfully.",
            "data": serializer.data,

        },status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Overrides the destroy method to add a custom response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "User deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)

