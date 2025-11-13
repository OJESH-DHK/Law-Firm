from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

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
    
class Client(models.Model):
    title = models.CharField(max_length=200, default="Our Clients")
    client_name = models.CharField(max_length=200)
    client_image = models.ImageField(upload_to='client_logos/')
    client_message = models.TextField(blank=True, null=True)
    practice_area = models.CharField(max_length=200, blank=True, null=True)
    practice_area_description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.client_name


class PracticeAreaMain(models.Model):
    main_title = models.CharField(max_length=200, default="Practice Areas")
    main_description = models.TextField()
    main_image = models.ImageField(upload_to='practice_area_images/', blank=True, null=True)
    practice_area = models.CharField(max_length=100)
    practice_area_description = models.TextField()

    def __str__(self):
        return self.main_title


class PracticeService(models.Model):
    main_section = models.ForeignKey(PracticeAreaMain, on_delete=models.CASCADE, related_name="services",blank=True, null=True)
    name = models.CharField(max_length=100)
    description = RichTextField()
    icon_image = models.ImageField(upload_to='practice_icons/', blank=True, null=True)

    def __str__(self):
        return self.name


    
class Attorney(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='attorney_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class PortfolioMain(models.Model):
    title = models.CharField(max_length=200, default="Our Portfolio")
    description = models.TextField()
    image = models.ImageField(upload_to='portfolio_images/')

    def __str__(self):
        return self.title
class PortfolioItem(models.Model):
    item_image = models.ImageField(upload_to='portfolio_items/')
    item_title = models.CharField(max_length=200)
    item_description = RichTextField()

    def __str__(self):
        return self.item_title
    
class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='author_images/', blank=True, null=True)

    def __str__(self):
        return self.name




class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name}"

class Index(models.Model):
    header = models.CharField(max_length=200, default="Welcome to Our Law Firm")
    sub_header = models.TextField()
    second_header = models.CharField(max_length=200, blank=True, null=True)
    second_sub_header = models.TextField(blank=True, null=True)
    second_image = models.ImageField(upload_to='index_images/', blank=True, null=True)

    def __str__(self):
        return self.header

class IndexBackgroundImage(models.Model):
    index = models.ForeignKey(Index, on_delete=models.CASCADE, related_name='background_images')
    image = models.ImageField(upload_to='index_images/')

class FreeLegalAdvice(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"


class LegalAdviceInfo(models.Model):
    image = models.ImageField(upload_to='legal_advice_images/')

    def __str__(self):
        return f"Legal Advice Image {self.id}"
    
class OrganizationInfo(models.Model):
    name = models.CharField(max_length=200)
    org_details = models.TextField()
    service_1 = models.CharField(max_length=200)
    service_2 = models.CharField(max_length=200)
    service_3 = models.CharField(max_length=200)
    service_4 = models.CharField(max_length=200)
    service_5 = models.CharField(max_length=200)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    org_logo = models.ImageField(upload_to='organization_logos/')

    def __str__(self):
        return self.name

    












