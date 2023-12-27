"""Models description."""

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """TimeStampedMixin described date fields."""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        """Abstraction."""

        abstract = True


class UUIDMixin(models.Model):
    """TimeStampedMixin described id field."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """Abstraction."""

        abstract = True


class Genre(TimeStampedMixin, UUIDMixin):
    """Genre described genre table."""

    name = models.CharField(_('genre'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self) -> str:
        """Return readable name."""
        return self.name

    class Meta:
        """Verbose names."""

        db_table = 'content\".\"genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class GenreFilmwork(UUIDMixin):
    """GenreFilmwork described genre table."""

    film_work = models.ForeignKey('filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Verbose names and db indexes."""

        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'], name='film_work_genre_idx'),
        ]
        db_table = 'content\".\"genre_film_work'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(TimeStampedMixin, UUIDMixin):
    """Person described person table."""

    full_name = models.CharField(_('full name'), blank=False)

    def __str__(self) -> str:
        """Return readable name."""
        return self.full_name

    class Meta:
        """Verbose names and db indexes."""

        indexes = [
            models.Index(fields=['full_name'], name='full_name_person'),
        ]
        db_table = 'content\".\"person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class PersonFilmwork(UUIDMixin):
    """PersonFilmwork described personFilmwork table."""

    class PersonFilmworkRole(models.TextChoices):
        """FilmworkType described options."""

        ACTOR = 'ACT', _('actor')
        DIRECTOR = 'DIR', _('director')
        WRITER = 'WRT', _('writer')

    film_work = models.ForeignKey('filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('person', on_delete=models.CASCADE)

    role = models.CharField(_('role'),
                            max_length=3,
                            choices=PersonFilmworkRole.choices,
                            default=PersonFilmworkRole.ACTOR,
                            )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Verbose names and db indexes."""

        indexes = [
            models.Index(fields=['film_work', 'person'], name='film_work_person_idx'),
        ]
        db_table = 'content\".\"person_film_work'
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class Filmwork(TimeStampedMixin, UUIDMixin):
    """Filmwork described filmwork table."""

    class FilmworkType(models.TextChoices):
        """FilmworkType described options."""

        MOVIE = 'MV', _('movie')
        TV_SHOW = 'TS', _('tv show')

    title = models.CharField(_('title'), blank=False, max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.CharField(_('creation date'), blank=False, max_length=50)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])

    type = models.CharField(_('type'),
                            max_length=2,
                            choices=FilmworkType.choices,
                            default=FilmworkType.MOVIE,
                            )

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self) -> str:
        """Return readable name."""
        return self.title

    class Meta:
        """Verbose names and db indexes."""

        indexes = [
            models.Index(fields=['creation_date', 'rating'], name='creation_date_rating'),
        ]
        db_table = 'content\".\"film_work'
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
