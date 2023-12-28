"""Declaration of API."""

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesApiMixin:
    """Aggregate and render data about filmwork, genres and persons."""

    model = Filmwork
    http_method_names = ['get']
    order = 'title'

    def get_queryset(self):
        """Aggregate data about film, genres and persons."""
        queryset = self.model.objects.get_queryset().order_by(self.order).values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
        ).prefetch_related('persons').annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=ArrayAgg('persons__full_name', distinct=True, filter=Q(personfilmwork__role='actor')),
            directors=ArrayAgg('persons__full_name', distinct=True, filter=Q(personfilmwork__role='director')),
            writers=ArrayAgg('persons__full_name', distinct=True, filter=Q(personfilmwork__role='writer')),
        )

        return queryset

    def render_to_response(self, context, **response_kwargs):
        """Return rendered data to client."""
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    """Return a list of filmworks with details."""

    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get(self, request, *args, **kwargs):
        """Describe basic GET method."""
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Collect data and pagination."""
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by,
        )

        prev = page.previous_page_number() if page.has_previous() else None
        next = page.next_page_number() if page.has_next() else None

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': prev,
            'next': next,
            'results': list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    """Return a filmwork with details found by id."""

    model = Filmwork
    http_method_names = ['get']

    def get(self, request, pk, *args, **kwargs):
        """Describe basic GET method."""
        context = self.get_context_data(pk)
        return self.render_to_response(context)

    def get_context_data(self, pk, **kwargs):
        """Return one record filtered by id."""
        queryset = self.get_queryset()
        record = queryset.filter(Q(id=pk))
        context = list(record)
        return context[0]
