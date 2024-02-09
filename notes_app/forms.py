from django import forms
from .models import Entry, Tag, Image, Link




# Custom models.py related forms

class EntryForm(forms.ModelForm):
    tag_names = forms.CharField(
        max_length=200, 
        required=False, 
        help_text="Enter tags separated by commas")

    class Meta:
        model = Entry
        fields = ['content']

# class TagForm(forms.ModelForm):
#     class Meta:
#         model = Tag
#         fields = ['name']

# class ImageForm(forms.ModelForm):
#     class Meta:
#         model = Image
#         fields = ['image']

# class LinkForm(forms.ModelForm):
#     class Meta:
#         model = Link
#         fields = ['url']