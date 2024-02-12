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


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['url']


class EntryFilterForm(forms.Form):
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label='Tag',
        empty_label="Select a tag"
    )
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
