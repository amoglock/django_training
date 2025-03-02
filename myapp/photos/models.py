from django.db import models
from django.utils.translation import gettext_lazy as _

class PhotoAlbum(models.Model):
    title = models.CharField(_('Название'), max_length=200)
    description = models.TextField(_('Описание'), blank=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)

    class Meta:
        verbose_name = _('Фотоальбом')
        verbose_name_plural = _('Фотоальбомы')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Photo(models.Model):
    album = models.ForeignKey(
        PhotoAlbum,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_('Альбом')
    )
    image = models.ImageField(_('Изображение'), upload_to='photos/%Y/%m/%d/')
    title = models.CharField(_('Название'), max_length=200)
    description = models.TextField(_('Описание'), blank=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Фотография')
        verbose_name_plural = _('Фотографии')
        ordering = ['-created_at']

    def __str__(self):
        return self.title 