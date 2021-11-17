from django import forms
from django.contrib import admin

from .models import Tag


class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'})
        }
        fields = '__all__'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    form = TagAdminForm
