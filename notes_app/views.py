from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from .models import Entry, Tag, Image, Link
from django.db.models import Q
from .forms import EntryForm
from django.contrib.auth.decorators import login_required





# ------------
# Navbar views
# ------------
@login_required
def profile(request):
    # Logic for displaying user profile
    return render(request, 'notes_app/profile.html')




# User Profile Settings views

# -----------
# Entry Views
# -----------


# Home page that also displays all entries, filtered by date
def home(request):
    entries = Entry.objects.filter(owner=request.user).order_by('-created_date')
    return render(request, 'notes_app/home.html', {'entries': entries})


# Displays the details of an entry
@login_required
def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    return render(request, 'notes_app/entry_detail.html', {'entry': entry})


# View function handling the forms necessary to create an entry
@login_required
def entry_create(request):
    ImageFormSet = inlineformset_factory(Entry, Image, fields=["image"], extra=1, can_delete=True)
    LinkFormSet = inlineformset_factory(Entry, Link, fields=["url"], extra=1, can_delete=True)
    
    if request.method == 'POST':
        form = EntryForm(request.POST)
        formset_images = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        formset_links = LinkFormSet(request.POST, queryset=Link.objects.none())
        
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
        formset_images = ImageFormSet(queryset=Image.objects.none())
        formset_links = LinkFormSet(queryset=Link.objects.none())
        
    context = {
        'form': form,
        'formset_images': formset_images,
        'formset_links': formset_links
    }
    return render(request, 'notes_app/entry_create.html', context)


# Function handling updating an already existing entry
@login_required
def edit_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    ImageFormSet = inlineformset_factory(Entry, Image, fields=["image"], extra=1, can_delete=True)  # calls image field from the Image model, related to Entry, w/ 1 extra field, can be deleted
    LinkFormSet = inlineformset_factory(Entry, Link, fields=["url"], extra=1, can_delete=True)  # calls image field from the Image model, related to Entry, w/ 1 extra field, can be deleted

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        formset_images = ImageFormSet(request.POST, request.FILES, instance=entry)
        formset_links = LinkFormSet(request.POST, instance=entry)

        if form.is_valid() and formset_images.is_valid() and formset_links.is_valid():
            # Currently the content in the entry and the tags are updating correctly
            entry = form.save()

            # Handle tags
            tag_names = request.POST.get('tags', '')
            tags = [Tag.objects.get_or_create(name=tag_name.strip())[0] for tag_name in tag_names.split(',')]
            entry.tags.set(tags)  # Associate the tags with the entry


            # Save images and links
            formset_images.save()
            formset_links.save()

            return redirect('notes_app:entry_detail', pk=entry.pk) #return redirect('entry_detail', pk=entry.pk)
    else:
        form = EntryForm(instance=entry)
        formset_images = ImageFormSet(instance=entry)
        formset_links = LinkFormSet(instance=entry)

    return render(request, 'notes_app/edit_entry.html', {
        'form': form,
        'formset_images': formset_images,
        'formset_links': formset_links,
        'entry': entry,  # Pass the entry to the template
    })


@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('entries_list')  # Redirect to the list of entries or wherever appropriate
    return render(request, 'notes_app/entry_confirm_delete.html', {'entry': entry})


# Search bar, this is completed and functioning as expected
@login_required
def search_results(request):
    query = request.GET.get('query', '')
    if query:
        entries = Entry.objects.filter(
            Q(content__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()
    else:
        entries = Entry.objects.all()

    return render(request, 'notes_app/search_results.html', {
        'entries': entries,
        'query': query
    })