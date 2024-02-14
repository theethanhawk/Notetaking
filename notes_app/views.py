"""This file handles rendering my entries, CRUD for entries"""

from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Entry, Tag, Image, Link
from .forms import EntryForm, EntryFilterForm, UserProfileForm


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'notes_app/profile.html', {'form': form})


def home(request):
    """Displayed home page for user w/ all of that users entries as well as filter funtionality""" 
    form = EntryFilterForm(request.GET)
    entries = Entry.objects.filter(owner=request.user).order_by('-created_date')

    if form.is_valid():
        if form.cleaned_data.get('tag'):
            entries = entries.filter(tags=form.cleaned_data['tag'])
        if form.cleaned_data.get('start_date'):
            entries = entries.filter(created_date__gte=form.cleaned_data['start_date'])
        if form.cleaned_data.get('end_date'):
            entries = entries.filter(created_date__lte=form.cleaned_data['end_date'])

    return render(request, 'notes_app/home.html', {'entries': entries, 'filter_form': form})


@login_required
def entry_detail(request, pk):
    """Renders details for the selected Entry"""
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'notes_app/entry_detail.html', {'entry': entry})


@login_required
def entry_create(request):
    """Renders forms with infline formsets and saves forms to create an Entry object"""
    image_formset = inlineformset_factory(Entry, Image, fields=["image"], extra=1)
    link_formset = inlineformset_factory(Entry, Link, fields=["url"], extra=1)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        formset_images = image_formset(request.POST, request.FILES, queryset=Image.objects.none())
        formset_links = link_formset(request.POST, queryset=Link.objects.none())

        if form.is_valid() and formset_images.is_valid() and formset_links.is_valid():
            entry = form.save(commit=False)
            entry.owner = request.user  # Assign the current user as the author
            entry.save()

            # Process tags
            tag_names = form.cleaned_data.get('tag_names')
            if tag_names:
                tag_names = [name.strip() for name in tag_names.split(',')]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    entry.tags.add(tag)

            # Save images
            formset_images.instance = entry
            formset_images.save()

            # Save links
            formset_links.instance = entry
            formset_links.save()

            return redirect('notes_app:entry_detail', pk=entry.pk)
    else:
        form = EntryForm()
        formset_images = image_formset(queryset=Image.objects.none())
        formset_links = link_formset(queryset=Link.objects.none())

    context = {
        'form': form,
        'formset_images': formset_images,
        'formset_links': formset_links,
    }
    return render(request, 'notes_app/entry_create.html', context)


# Function handling updating an already existing entry
@login_required
def edit_entry(request, pk):
    """Renders entry details in an editable instance"""
    entry = get_object_or_404(Entry, pk=pk)
    image_formset = inlineformset_factory(Entry, Image, fields=["image"], can_delete=True, extra=1)
    link_formset = inlineformset_factory(Entry, Link, fields=["url"], can_delete=True, extra=1)

    if request.method == 'POST':
        # print state helps me see what is happening at the post, helps me debug
        print(request.POST)
        form = EntryForm(request.POST, instance=entry)
        formset_images = image_formset(request.POST, request.FILES, instance=entry)
        formset_links = link_formset(request.POST, instance=entry)

        if form.is_valid() and formset_images.is_valid() and formset_links.is_valid():
            # Currently the content in the entry and the tags are updating correctly
            entry = form.save()

            # Handle tags
            tag_names = request.POST.get('tags', '')
            tags = [
                Tag.objects.get_or_create(name=tag_name.strip())[0]
                    for tag_name in tag_names.split(',')
                ]
            entry.tags.set(tags)  # Associate the tags with the entry

            # Manually delete images and links marked for deletion
                # Images
            for form in formset_images.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

                # Links
            for form in formset_links.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()


            # Save images and links
            formset_images.save()
            formset_links.save()

            return redirect('notes_app:entry_detail', pk=entry.pk)
    else:
        form = EntryForm(instance=entry)
        formset_images = image_formset(instance=entry)
        formset_links = link_formset(instance=entry)

    return render(request, 'notes_app/edit_entry.html', {
        'form': form,
        'formset_images': formset_images,
        'formset_links': formset_links,
        'entry': entry,  # Pass the entry to the template
    })


@login_required
def entry_delete(request, pk):
    """Renders a delete box inside the editable entry view"""
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('notes_app:home')  # Redirect to the list of entries or wherever appropriate
    return render(request, 'notes_app/confirm_entry_delete.html', {'entry': entry})


# Search bar, this is completed and functioning as expected
@login_required
def search_results(request):
    """Provides functionality to the search bar"""
    query = request.GET.get('query', '')
    if query:
        entries = Entry.objects.filter(
            Q(content__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()
    else:
        entries = Entry.objects.all()

    return render(request, 'notes_app/search_results.html', {
        'entries': entries,
        'query': query,
    })
