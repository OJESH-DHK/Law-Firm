from django.shortcuts import render, redirect, get_object_or_404
from apps.models import *
from django.contrib import messages
from django.core.paginator import Paginator


def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def ad_contact(request):
    # Get the latest contact info (address, phone, email, website)
    contact_info = ContactInfo.objects.last()

    # Get the latest contact page section (header, sub_header, image, map)
    contact_section = Contact.objects.last()

    # Get all contact messages, newest first
    messages_list = ContactMessage.objects.all().order_by('-created_at')

    context = {
        "contact_info": contact_info,
        "contact_section": contact_section,
        "messages_list": messages_list
    }
    return render(request, 'dashboard/ad_contact/ad_contact.html', context)





# ----- Edit Contact Info -----
def edit_contact_info(request, id):
    contact_info = get_object_or_404(ContactInfo, id=id)

    if request.method == "POST":
        contact_info.address = request.POST.get("address")
        contact_info.phone = request.POST.get("phone")
        contact_info.email = request.POST.get("email")
        contact_info.website = request.POST.get("website")
        contact_info.save()

        messages.success(request, "Contact information updated successfully!")
        return redirect("ad_contact")

    return render(request, "dashboard/ad_contact/edit_contact_info.html", {"contact_info": contact_info})


# ----- Edit Contact Section -----
def edit_contact_section(request, id):
    contact_section = get_object_or_404(Contact, id=id)

    if request.method == "POST":
        contact_section.header = request.POST.get("header")
        contact_section.sub_header = request.POST.get("sub_header")
        contact_section.map_embed_code = request.POST.get("map_embed_code")

        # Handle optional image upload
        if request.FILES.get("image"):
            contact_section.image = request.FILES.get("image")

        contact_section.save()
        messages.success(request, "Contact section updated successfully!")
        return redirect("ad_contact")

    return render(request, "dashboard/ad_contact/edit_contact_section.html", {"contact_section": contact_section})





# ----- Delete Contact Message -----
def delete_contact_message(request, id):
    msg = get_object_or_404(ContactMessage, id=id)
    msg.delete()
    messages.success(request, "Message deleted successfully!")
    return redirect("ad_contact")




def dashboard_gallery(request):
    # Fetch the latest gallery
    gallery = Gallery.objects.last()

    # If no gallery exists yet, create one
    if not gallery:
        gallery = Gallery.objects.create(title="See Our Gallery")

    # Handle gallery info update
    if request.method == "POST" and "update_gallery" in request.POST:
        gallery.title = request.POST.get("title")
        gallery.description = request.POST.get("description")

        # Replace header image only if a new one is uploaded
        if "header_image" in request.FILES:
            gallery.header_image = request.FILES["header_image"]

        gallery.save()
        messages.success(request, "Gallery information updated successfully!")
        return redirect("dashboard_gallery")

    # Handle new image upload
    if request.method == "POST" and "add_image" in request.POST:
        image = request.FILES.get("image")
        if image:
            GalleryImage.objects.create(gallery=gallery, image=image)
            messages.success(request, "Image added successfully!")
        else:
            messages.error(request, "Please select an image before uploading.")
        return redirect("dashboard_gallery")

    # Fetch all images for pagination
    images = GalleryImage.objects.filter(gallery=gallery).order_by("-id")
    paginator = Paginator(images, 6)
    page_number = request.GET.get("page")
    paged_images = paginator.get_page(page_number)

    return render(request, "dashboard/gallery/ad_gallery.html", {
        "gallery": gallery,
        "images": paged_images,
    })


def delete_gallery_image(request, id):
    image = get_object_or_404(GalleryImage, id=id)
    image.delete()
    messages.success(request, "Image deleted successfully!")
    return redirect("dashboard_gallery")


# Dashboard list view
def about_dashboard(request):
    about_list = AboutUs.objects.all().order_by('-id')
    
    return render(request, 'dashboard/about/ad_about.html', {'about_list': about_list})



# Delete About record
def admin_delete_about(request, id):
    about = get_object_or_404(AboutUs, id=id)
    about.delete()
    messages.success(request, "About record deleted successfully!")
    return redirect('about_dashboard')






