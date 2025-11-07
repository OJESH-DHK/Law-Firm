from django.db import models

class ContactInfo(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contact Info ({self.id})"

class Contact(models.Model):
    header = models.CharField(max_length=200)
    sub_header = models.TextField()
    image = models.ImageField(upload_to='contact_images/')
    map_embed_code = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.header


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.first_name} {self.last_name}"

from django.db import models

class Gallery(models.Model):
    title = models.CharField(max_length=200, default="See Our Gallery")
    header_image = models.ImageField(upload_to='gallery_images/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery_images/')

    def __str__(self):
        return f"{self.gallery.title} Image"
    
class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='about_us_images/', blank=True, null=True)
    second_image = models.ImageField(upload_to='about_us_images/', blank=True, null=True)
    second_title = models.CharField(max_length=200, blank=True, null=True)
    second_description = models.TextField(blank=True, null=True)
    attorneys_name = models.CharField(max_length=200, blank=True, null=True)
    attorney_dsescription = models.TextField(blank=True, null=True)
    attorney_position = models.TextField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    attorney_image = models.ImageField(upload_to='about_us_images/', blank=True, null=True)
    third_title = models.CharField(max_length=200, blank=True, null=True)
    third_description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title








