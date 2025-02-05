from django.conf import settings
import auto_prefetch
from django.db import models
from django.db.models import Func, Value
from django.db.models.lookups import LessThanOrEqual

from .articles import Article


class ForumSection(auto_prefetch.Model):
    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "Категория форума"
        verbose_name_plural = "Категории форума"

    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    order = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True)
    # this is hidden for anyone unless they click "show hidden"
    is_hidden = models.BooleanField(verbose_name="Скрытая категория", default=False)
    # this is displayed for moderators and admins but completely hidden for users
    is_hidden_for_users = models.BooleanField(verbose_name="Видима только модераторам", default=False)

    def __str__(self):
        return self.name


class ForumCategory(auto_prefetch.Model):
    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "Раздел форума"
        verbose_name_plural = "Разделы форума"

    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    order = models.IntegerField(verbose_name="Порядок сортировки", default=0, blank=True)
    section = auto_prefetch.ForeignKey(ForumSection, on_delete=models.DO_NOTHING, verbose_name="Категория")  # to-do: review later
    is_for_comments = models.BooleanField(verbose_name="Отображать комментарии к статьям в этом разделе", default=False)

    def __str__(self):
        return self.name


class ForumThread(auto_prefetch.Model):
    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "Тема форума"
        verbose_name_plural = "Темы форума"

        constraints = [
            # logic: a thread must have either 'article' or 'category' assigned
            # requires postgres >9.2
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_category_or_article',
                check=LessThanOrEqual(
                    lhs=Func('article_id', 'category_id', function='num_nonnulls', output_field=models.IntegerField()),
                    rhs=Value(1),
                ),
            )
        ]

    name = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Время изменения")
    category = auto_prefetch.ForeignKey(ForumCategory, on_delete=models.DO_NOTHING, null=True, verbose_name="Раздел (если это тема)")  # to-do: review later
    article = auto_prefetch.ForeignKey(Article, on_delete=models.CASCADE, null=True, verbose_name="Статья (если это комментарии)")
    author = auto_prefetch.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Автор")
    is_pinned = models.BooleanField(verbose_name="Пришпилено", default=False)
    is_locked = models.BooleanField(verbose_name="Закрыто", default=False)


class ForumPost(auto_prefetch.Model):
    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "Сообщение форума"
        verbose_name_plural = "Сообщения форума"

    name = models.TextField(verbose_name="Название", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Время изменения")
    author = auto_prefetch.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Автор")
    reply_to = auto_prefetch.ForeignKey(to='ForumPost', on_delete=models.SET_NULL, null=True, verbose_name="Ответ на комментарий")
    thread = auto_prefetch.ForeignKey(to=ForumThread, on_delete=models.CASCADE, verbose_name="Тема")


class ForumPostVersion(auto_prefetch.Model):
    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "Версия сообщения форума"
        verbose_name_plural = "Версии сообщений форума"

    post = auto_prefetch.ForeignKey(to=ForumPost, on_delete=models.CASCADE, verbose_name="Сообщение")
    source = models.TextField(verbose_name="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    author = auto_prefetch.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Автор правки")
