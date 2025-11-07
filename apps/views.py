from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *



#index page view
def index(request):
    return render(request, 'ui/index.html')

#about page view
def about(request):
    latest_info = AboutUs.objects.last()
    # Get all records for the specific fields you want to loop
    attorneys_info = AboutUs.objects.all().values(
        'attorneys_name', 
        'attorney_dsescription', 
        'attorney_position',
        'facebook_link',
        'twitter_link',
        'linkedin_link',
        'instagram_link',
        'attorney_image',
        
    )
    return render(request, 'ui/about.html', {
        "latest_info": latest_info,
        "attorneys_info": attorneys_info
    })

#main blog view 
def blog_main(request):
    return render(request, 'ui/blog.html')

#blog-single page view
def blog_single(request, id):
    return render(request, 'ui/blog-single.html')


#contact page view
def contact(request):
    contact = ContactInfo.objects.last()
    contact_section = Contact.objects.last()
    
    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        
        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact") 

    return render(request, "ui/contact.html", {"contact": contact , "contact_section": contact_section})



def gallery(request):
    # Get the latest gallery
    gallery = Gallery.objects.last()
    
    # Get all images for that gallery
    all_images = GalleryImage.objects.filter(gallery=gallery).order_by('-id')
    
    # Paginate: 6 images per page
    paginator = Paginator(all_images, 6)
    page_number = request.GET.get('page')
    images = paginator.get_page(page_number)
    
    return render(request, "ui/gallery.html", {
        "gallery": gallery,
        "images": images
    })



#main page view
def main(request):
    return render(request, 'ui/main.html')

#practice page view
def practice(request):
    return render(request, 'ui/practice.html')
#portfolio page view
def portfolio(request):
    return render(request, 'ui/won.html')
