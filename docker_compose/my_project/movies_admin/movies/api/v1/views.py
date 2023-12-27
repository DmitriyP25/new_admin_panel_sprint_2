"""Declaration of API."""

# from django.contrib.postgres.aggregates import ArrayAgg
# from django.db.models import Q
from django.http import JsonResponse
# from django.views import View
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesApiMixin:
    """Docstring in public class."""
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        """Docstring in public method."""
        return  # Сформированный QuerySet

    def render_to_response(self, context, **response_kwargs):
        """Docstring in public method."""
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    """Docstring in public class."""

    model = Filmwork
    http_method_names = ['get']  # Список методов, которые реализует обработчик

    def get(self, request, *args, **kwargs):
        """Docstring in public method."""
        # Получение и обработка данных
        return JsonResponse({})

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     """Docstring in public method."""
    #     queryset = self.get_queryset()
    #     paginator, page, queryset, is_paginated = self.paginate_queryset(
    #         queryset,
    #         self.paginate_by,
    #     )
    #     context = {
    #         'count': paginator.count,
    #         'total_pages': int,
    #         'prev': int,
    #         'next': int,
    #         'results': list(self.get_queryset()),
    #     }
    #     return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return  # Словарь с данными объекта
