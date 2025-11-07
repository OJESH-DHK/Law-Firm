from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ContactInfo)
admin.site.register(Contact)
admin.site.register(ContactMessage)
admin.site.register(AboutUs)



# Inline for multiple images
class GalleryImageInline(admin.TabularInline):  # or admin.StackedInline
    model = GalleryImage
    extra = 3  # How many empty forms to show by default
    max_num = 20  # optional: max number of images

# Register Gallery with inline images
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]
    list_display = ('title',)

