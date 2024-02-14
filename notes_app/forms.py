from django import forms
from .models import Entry, Tag, Image, Link, UserProfile


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
    """This form helps me filter entries on the home page"""
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label='Tag',
        empty_label="Select a tag"
    )
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'theme_preference']
        widgets = {
            'theme_preference': forms.Select(attrs={'id':'id_theme_preference'}),
        }