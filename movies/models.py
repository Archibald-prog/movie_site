from django.db import models
from django.urls import reverse
from datetime import date

from modules.services.utils import gen_slug


class Category(models.Model):
    """Категории"""
    name = models.CharField(verbose_name="Категория", max_length=150)
    slug = models.SlugField(max_length=160, blank=True, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    """Актеры и режиссеры"""
    name = models.CharField(verbose_name="Имя", max_length=100)
    slug = models.SlugField(max_length=255, blank=True, unique=True, db_index=True, verbose_name="URL")
    age = models.PositiveSmallIntegerField(verbose_name="Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField(verbose_name="Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField(verbose_name="Имя", max_length=100)
    slug = models.SlugField(max_length=160, blank=True, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """Фильм"""
    title = models.CharField(verbose_name="Название", max_length=255)
    slug = models.SlugField(max_length=255, blank=True, unique=True, db_index=True, verbose_name="URL")
    tagline = models.CharField(verbose_name="Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    poster = models.ImageField(verbose_name="Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField(verbose_name="Дата выхода", default=2019)
    country = models.CharField(verbose_name="Страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField(verbose_name="Премьера в мире", default=date.today)
    budget = models.PositiveIntegerField(verbose_name="Бюджет", default=0,
                                         help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        verbose_name="Сборы в США", default=0, help_text="указывать сумму в долларах"
    )
    fees_in_world = models.PositiveIntegerField(
        verbose_name="Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    draft = models.BooleanField(verbose_name="Черновик", default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gen_slug(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.slug})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField(verbose_name="Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField(verbose_name="Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
