from django.db import models

class Blog(models.Model):
    """
    Модель блога.

    Хранит информацию о статье, такую как заголовок, содержание, дата публикации, автор, статус публикации и т.п.
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Введите заголовок статьи (до 200 символов)"
    )
    text = models.TextField(
        verbose_name="Содержание",
        help_text="Введите содержание статьи"
    )
    author = models.CharField(
        max_length=100,
        verbose_name="Автор",
        help_text="Имя автора статьи"
    )
    published_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего обновления"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL-адрес",
        help_text="Уникальный URL-идентификатор статьи"
    )

    class Meta:
        db_table = 'blog_posts'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
        ]
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            # Проверяем, существует ли такой slug, и добавляем суффикс, пока не найдем уникальный
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)