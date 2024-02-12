from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# Entry related models

class Tag(models.Model):
    """Tag for categorizing entries"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """Returns a string representation of the tag"""
        return f"{self.name}"
    

class Entry(models.Model):
    """Entry object displaying portion of content along with tags"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a string representation of the model"""
        return f"{self.content[:50]}..."
    

class Image(models.Model):
    """Simple image containing model related to entry through foreign key"""
    entry = models.ForeignKey(Entry, related_name='images', on_delete=models.CASCADE)
    # image field does not work for all image types, this needs updating
    # in settings directs to upload to notetaking/media/images/
    image = models.ImageField(
        upload_to='images/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'xml'])],
    )

    def __str__(self):
        return f'Image {self.id} for Entry {self.entry.id}'


class Link(models.Model):
    """Simple model with one field for adding a url, related to entry through foreign key"""
    entry = models.ForeignKey(Entry, related_name='links', on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f'Link {self.id} for Entry {self.entry.id}'
    