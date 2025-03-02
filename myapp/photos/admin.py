from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.urls import path, reverse
from django.contrib import messages
from django.http import HttpResponse
from .models import PhotoAlbum, Photo
from .forms import PhotoAdminForm

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3  # количество пустых форм для загрузки
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
        print(f"Content type: {request.content_type}")
        print(f"Request headers: {request.headers}")
        
        if request.method == 'POST':
            print("\n=== POST Data ===")
            print("FILES:", request.FILES)
            print("POST:", request.POST)
            print("Content Type:", request.content_type)
            
            try:
                album = PhotoAlbum.objects.get(id=album_id)
                files = request.FILES.getlist('photos')
                
                print("\n=== Files ===")
                print("Files list:", files)
                print("Number of files:", len(files))
                
                if not files:
                    print("No files found in request")
                    messages.error(request, 'Не выбраны файлы для загрузки')
                    return redirect('admin:photos_photoalbum_change', album_id)
                
                for file in files:
                    print(f"\nProcessing file: {file.name}")
                    print(f"File size: {file.size}")
                    print(f"File content type: {file.content_type}")
                    Photo.objects.create(
                        album=album,
                        image=file,
                        title=file.name,
                    )
                messages.success(request, f'Успешно загружено {len(files)} фотографий')
            except PhotoAlbum.DoesNotExist:
                print("Album not found:", album_id)
                messages.error(request, 'Альбом не найден')
            except Exception as e:
                print(f"Error: {str(e)}")
                print(f"Error type: {type(e)}")
                messages.error(request, f'Ошибка при загрузке фотографий: {str(e)}')
            
            return redirect('admin:photos_photoalbum_change', album_id)
        
        return HttpResponse('Method not allowed', status=405)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        print("\n=== Change View Called ===")
        print(f"Object ID: {object_id}")
        print(f"Request path: {request.path}")
        print(f"Request method: {request.method}")
        
        extra_context = extra_context or {}
        extra_context['show_upload_button'] = True
        upload_url = reverse(
            'admin:photos_photoalbum_upload-multiple',
            args=[object_id]
        )
        print(f"Generated upload URL: {upload_url}")
        print(f"Extra context: {extra_context}")
        extra_context['upload_url'] = upload_url
        
        response = super().change_view(request, object_id, form_url, extra_context=extra_context)
        print("Change view response type:", type(response))
        print("Change view response:", response)
        return response

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    form = PhotoAdminForm
    list_display = ['title', 'album', 'created_at']
    list_filter = ['album', 'created_at']
    search_fields = ['title', 'description']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if form.cleaned_data.get('multiple_photos'):
            album = obj.album
            files = request.FILES.getlist('multiple_photos')
            
            try:
                for file in files:
                    Photo.objects.create(
                        album=album,
                        image=file,
                        title=file.name,
                    )
                messages.success(request, f'Успешно загружено {len(files)} дополнительных фотографий')
            except Exception as e:
                messages.error(request, f'Ошибка при загрузке дополнительных фотографий: {str(e)}')
    