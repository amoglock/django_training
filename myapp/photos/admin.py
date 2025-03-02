from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.urls import path, reverse
from django.contrib import messages
from .models import PhotoAlbum, Photo
from .forms import PhotoAdminForm

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3
    fields = ['image', 'title', 'description']

@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    search_fields = ['title', 'description']
    inlines = [PhotoInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:album_id>/upload-multiple/',
                self.admin_site.admin_view(self.upload_multiple),
                name='photos_photoalbum_upload-multiple',
            ),
        ]
        return custom_urls + urls

    def upload_multiple(self, request, album_id):
        print("\n=== Upload Multiple Called ===")
        print(f"Requested URL: {request.path}")
        print(f"Album ID: {album_id}")
        print(f"Request method: {request.method}")
        
        if request.method == 'POST':
            try:
                album = PhotoAlbum.objects.get(id=album_id)
                files = request.FILES.getlist('photos')
                
                if not files:
                    messages.error(request, 'Не выбраны файлы для загрузки')
                    return redirect('admin:photos_photoalbum_change', album_id)
                
                for file in files:
                    Photo.objects.create(
                        album=album,
                        image=file,
                        title=file.name,
                    )
                messages.success(request, f'Успешно загружено {len(files)} фотографий')
            except PhotoAlbum.DoesNotExist:
                messages.error(request, 'Альбом не найден')
            except Exception as e:
                messages.error(request, f'Ошибка при загрузке фотографий: {str(e)}')
            
            return redirect('admin:photos_photoalbum_change', album_id)
        
        return HttpResponse('Method not allowed', status=405)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_upload_button'] = True
        upload_url = reverse(
            'admin:photos_photoalbum_upload-multiple',
            args=[object_id]
        )
        extra_context['upload_url'] = upload_url
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    form = PhotoAdminForm
    list_display = ['title', 'album', 'created_at']
    list_filter = ['album', 'created_at']
    search_fields = ['title', 'description']