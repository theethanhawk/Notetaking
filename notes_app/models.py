from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


# User Profile models



# Entry related models here.    

class Tag(models.Model):
    """Tag for categorizing entries"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """Returns a string representation of the tag"""
        return f"#{self.name}"
    

class Entry(models.Model):
    """Entry within a specific Topic"""
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
    entry = models.ForeignKey(Entry, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='images/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'xml'])],
        # As of right now not all image types work, might be due to size or type, update pending
        # Consider building a script that converts images to the appropriate file type or a similar method
        # For now any file that does not work I use the snip tool to convert, but this is a cheap workaround
    )

    def __str__(self):
        return f'Image {self.id} for Entry {self.entry.id}'

class Link(models.Model):
    entry = models.ForeignKey(Entry, related_name='links', on_delete=models.CASCADE)
    url = models.URLField()

    def __str__(self):
        return f'Link {self.id} for Entry {self.entry.id}'
    
