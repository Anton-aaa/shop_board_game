from rest_framework import filters


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_staff:
            return queryset.filter()

        return queryset.filter(client=request.user)