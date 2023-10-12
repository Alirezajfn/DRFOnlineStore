from rest_framework.filters import BaseFilterBackend


class SelfFilterBacked(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(username=request.user.username)
        return queryset
