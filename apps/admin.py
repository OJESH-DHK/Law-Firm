from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Index)
admin.site.register(IndexBackgroundImage)
admin.site.register(ContactInfo)
admin.site.register(Contact)
admin.site.register(ContactMessage)
admin.site.register(AboutUs)
admin.site.register(Client)
admin.site.register(PortfolioMain)
admin.site.register(PortfolioItem)
admin.site.register(Blog)
admin.site.register(BlogPost)
admin.site.register(Author)
admin.site.register(Attorney)
admin.site.register(PracticeAreaMain)
admin.site.register(PracticeService)
admin.site.register(FreeLegalAdvice)
admin.site.register(LegalAdviceInfo)
admin.site.register(OrganizationInfo)


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

