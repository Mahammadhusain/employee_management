from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from .models import User
from django.db.models import Q

class UserFilter(FilterSet):
    """
    Filter class for User model.
    """
    q = CharFilter(method='filter_query', label='Search query (name or email)')

    class Meta:
        model = User
        fields = ['q', 'role']

    def filter_query(self, queryset, name, value):
        """
        Custom filter method to search by name or email.
        """
        return queryset.filter(Q(name__icontains=value) | Q(email__icontains=value))