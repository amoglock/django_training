from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Photo, PhotoAlbum

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class PhotoAdminForm(forms.ModelForm):
    multiple_photos = forms.FileField(
        required=False,
        widget=MultipleFileInput(),
        label='Загрузить несколько фотографий'
    )

    class Meta:
        model = Photo
        fields = '__all__' 