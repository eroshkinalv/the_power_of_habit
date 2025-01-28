from rest_framework.filters import BaseFilterBackend


class IsPublicFilterBackend(BaseFilterBackend):
    """
    Позволяет пользователям видеть свои привычки и привычки, опубликованные в общий доступ.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(is_public=True) | queryset.filter(owner=request.user)
