"""Classes for admin panel in django project."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from movies.models import (Filmwork, Genre, GenreFilmwork, Person,
                           PersonFilmwork)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """The GenreAdmin class shows which fields will be shown."""

    list_filter = ('name',)
    search_fields = ('name',)


class GenreFilmworkInline(admin.TabularInline):
    """The GenreFilmworkInline class shows the associated model."""

    model = GenreFilmwork
    autocomplete_fields = ['genre']
    verbose_name = _('genre')
    verbose_name_plural = _('genres')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """The PersonAdmin class shows which fields will be shown."""

    list_filter = ('full_name',)
    search_fields = ('full_name',)


class PersonFilmworkInline(admin.TabularInline):
    """The PersonFilmworkInline class shows the associated model."""

    model = PersonFilmwork
    autocomplete_fields = ['person']
    verbose_name = _('person')
    verbose_name_plural = _('persons')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """The PersonAdmin class shows which fields will be shown."""

    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')
    list_display = (
        'title',
        'type',
        'get_genres',
        'get_persons',
        'creation_date',
        'rating',
    )

    list_prefetch_related = ('genres', 'persons')

    def get_queryset(self, request):
        """Return queryset for prefetch related list."""
        queryset = (
            super() .get_queryset(request).prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        """Return queryset of filmwork genres."""
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'

    def get_persons(self, obj):
        """Return queryset of filmwork participators."""
        return ','.join([person.full_name for person in obj.persons.all()])

    get_persons.short_description = 'В фильме приняли участие'
