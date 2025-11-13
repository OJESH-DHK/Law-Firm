from django.shortcuts import render, redirect, get_object_or_404
from apps.models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # redirect if already logged in

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # redirect after login
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        
        user = request.user

        # Check current password
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('change_password')

        # Check new password match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('change_password')

        # Set new password
        user.set_password(new_password)
        user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password changed successfully!")
        return redirect('dashboard')

    return render(request, "change_password.html")



@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


@login_required(login_url='login')
def admin_index_dashboard(request):
    index_data = Index.objects.all()
    return render(request, 'dashboard/index/admin_index.html', {'index_data': index_data})

@login_required(login_url='login')
def edit_index(request, id):
    index = get_object_or_404(Index, id=id)

    if request.method == 'POST':
        # Update main fields
        index.header = request.POST.get('header')
        index.sub_header = request.POST.get('sub_header')
        index.second_header = request.POST.get('second_header')
        index.second_sub_header = request.POST.get('second_sub_header')  # ← Add this line

        if 'second_image' in request.FILES:
            index.second_image = request.FILES['second_image']

        index.save()

        # Handle new background images (up to 3)
        bg_files = request.FILES.getlist('background_images')
        for file in bg_files:
            if file:  # skip empty file inputs
                IndexBackgroundImage.objects.create(index=index, image=file)

        messages.success(request, "Homepage section updated successfully.")
        return redirect('dashboard_index')

    return render(request, 'dashboard/index/edit_index.html', {'index': index})





@login_required(login_url='login')
def delete_bg_image(request, id):
    """
    Delete a single background image from a homepage section.
    """
    bg_image = get_object_or_404(IndexBackgroundImage, id=id)
    index_id = bg_image.index.id
    bg_image.delete()
    messages.success(request, "Background image deleted successfully.")
    return redirect('dashboard_edit_index', id=index_id)

@login_required(login_url='login')
def delete_index(request, id):
    index_section = get_object_or_404(Index, id=id)
    

    for bg in index_section.background_images.all():
        if bg.image:
            bg.image.delete(save=False) 
        bg.delete()
    
    if index_section.second_image:
        index_section.second_image.delete(save=False)
    
    index_section.delete()
    messages.success(request, "Homepage section deleted successfully.")
    return redirect('admin_index_dashboard')



@login_required(login_url='login')
def ad_contact(request):
    contact_info = ContactInfo.objects.last()
    contact_section = Contact.objects.last()
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    context = {
        "contact_info": contact_info,
        "contact_section": contact_section,
        "messages_list": messages_list
    }
    return render(request, 'dashboard/ad_contact/ad_contact.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def edit_contact_section(request, id):
    contact_section = get_object_or_404(Contact, id=id)
    if request.method == "POST":
        contact_section.header = request.POST.get("header")
        contact_section.sub_header = request.POST.get("sub_header")
        contact_section.map_embed_code = request.POST.get("map_embed_code")
        if request.FILES.get("image"):
            contact_section.image = request.FILES.get("image")
        contact_section.save()
        messages.success(request, "Contact section updated successfully!")
        return redirect("ad_contact")
    return render(request, "dashboard/ad_contact/edit_contact_section.html", {"contact_section": contact_section})


@login_required(login_url='login')
def delete_contact_message(request, id):
    msg = get_object_or_404(ContactMessage, id=id)
    msg.delete()
    messages.success(request, "Message deleted successfully!")
    return redirect("ad_contact")


@login_required(login_url='login')
def dashboard_gallery(request):
    gallery = Gallery.objects.last()
    if not gallery:
        gallery = Gallery.objects.create(title="See Our Gallery")

    if request.method == "POST" and "update_gallery" in request.POST:
        gallery.title = request.POST.get("title")
        gallery.description = request.POST.get("description")
        if "header_image" in request.FILES:
            gallery.header_image = request.FILES["header_image"]
        gallery.save()
        messages.success(request, "Gallery information updated successfully!")
        return redirect("dashboard_gallery")

    if request.method == "POST" and "add_image" in request.POST:
        image = request.FILES.get("image")
        if image:
            GalleryImage.objects.create(gallery=gallery, image=image)
            messages.success(request, "Image added successfully!")
        else:
            messages.error(request, "Please select an image before uploading.")
        return redirect("dashboard_gallery")

    images = GalleryImage.objects.filter(gallery=gallery).order_by("-id")
    paginator = Paginator(images, 6)
    page_number = request.GET.get("page")
    paged_images = paginator.get_page(page_number)
    return render(request, "dashboard/gallery/ad_gallery.html", {
        "gallery": gallery,
        "images": paged_images,
    })


@login_required(login_url='login')
def delete_gallery_image(request, id):
    image = get_object_or_404(GalleryImage, id=id)
    image.delete()
    messages.success(request, "Image deleted successfully!")
    return redirect("dashboard_gallery")


@login_required(login_url='login')
def dashboard_about(request):
    about_entries = AboutUs.objects.all()
    attorneys = Attorney.objects.all()
    clients = Client.objects.all()
    return render(request, 'dashboard/about/about_dashboard.html', {
        'about_entries': about_entries,
        'attorneys': attorneys,
        'clients': clients
    })


@login_required(login_url='login')
def edit_about(request, id):
    about_entry = get_object_or_404(AboutUs, id=id)
    if request.method == "POST":
        about_entry.title = request.POST.get('title')
        about_entry.description = request.POST.get('description')
        about_entry.second_title = request.POST.get('second_title')
        about_entry.second_description = request.POST.get('second_description')
        about_entry.third_title = request.POST.get('third_title')
        about_entry.third_description = request.POST.get('third_description')
        if request.FILES.get('image'):
            about_entry.image = request.FILES['image']
        if request.FILES.get('second_image'):
            about_entry.second_image = request.FILES['second_image']
        about_entry.save()
        messages.success(request, "About entry updated successfully!")
        return redirect('dashboard_about')
    return render(request, 'dashboard/about/edit_about.html', {'about_entry': about_entry})


@login_required(login_url='login')
def admin_add_attorney(request):
    if request.method == 'POST':
        Attorney.objects.create(
            name=request.POST['name'],
            description=request.POST.get('description'),
            position=request.POST.get('position'),
            facebook_link=request.POST.get('facebook_link'),
            twitter_link=request.POST.get('twitter_link'),
            linkedin_link=request.POST.get('linkedin_link'),
            instagram_link=request.POST.get('instagram_link'),
            image=request.FILES.get('image')
        )
        messages.success(request, 'Attorney added successfully!')
        return redirect('dashboard_attorneys')
    return render(request, 'dashboard/about/add_attorney.html')


@login_required(login_url='login')
def edit_attorney(request, id):
    attorney = get_object_or_404(Attorney, id=id)
    if request.method == 'POST':
        attorney.name = request.POST['name']
        attorney.description = request.POST.get('description')
        attorney.position = request.POST.get('position')
        attorney.facebook_link = request.POST.get('facebook_link')
        attorney.twitter_link = request.POST.get('twitter_link')
        attorney.linkedin_link = request.POST.get('linkedin_link')
        attorney.instagram_link = request.POST.get('instagram_link')
        if request.FILES.get('image'):
            attorney.image = request.FILES['image']
        attorney.save()
        messages.success(request, 'Attorney updated successfully!')
        return redirect('dashboard_attorneys')
    return render(request, 'dashboard/about/edit_attorney.html', {'attorney': attorney})


@login_required(login_url='login')
def delete_attorney(request, id):
    attorney = get_object_or_404(Attorney, id=id)
    attorney.delete()
    messages.success(request, 'Attorney deleted successfully!')
    return redirect('dashboard_attorneys')


# --------- Portfolio Views ---------
@login_required(login_url='login')
def admin_portfolio(request):
    portfolio_main = PortfolioMain.objects.last()
    portfolio_items_list = PortfolioItem.objects.all()
    paginator = Paginator(portfolio_items_list, 10)
    page_number = request.GET.get('page')
    portfolio_items = paginator.get_page(page_number)
    clients = Client.objects.all()
    context = {
        'portfolio_main': portfolio_main,
        'portfolio_items': portfolio_items,
        'clients': clients
    }
    return render(request, 'dashboard/portfolio/admin_portfolio.html', context)


@login_required(login_url='login')
def admin_edit_portfolio_main(request, id):
    portfolio_main = get_object_or_404(PortfolioMain, id=id)
    if request.method == 'POST':
        portfolio_main.title = request.POST.get('title')
        portfolio_main.description = request.POST.get('description')
        if request.FILES.get('image'):
            portfolio_main.image = request.FILES.get('image')
        portfolio_main.save()
        messages.success(request, 'Portfolio Main updated successfully!')
        return redirect('admin_portfolio')
    return render(request, 'dashboard/portfolio/admin_edit_portfolio_main.html', {'portfolio_main': portfolio_main})


@login_required(login_url='login')
def admin_edit_client(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == 'POST':
        client.client_name = request.POST.get('name')
        client.client_message = request.POST.get('message')
        if request.FILES.get('image'):
            client.client_image = request.FILES.get('image')
        client.save()
        messages.success(request, "Client updated successfully!")
        return redirect('dashboard_clients')
    return render(request, 'dashboard/portfolio/admin_edit_client.html', {'client': client})


@login_required(login_url='login')
def admin_delete_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    messages.success(request, "Client deleted successfully!")
    return redirect('dashboard_clients')


@login_required(login_url='login')
def admin_add_client(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        image = request.FILES.get('image')
        Client.objects.create(
            client_name=name,
            client_message=message,
            client_image=image
        )
        messages.success(request, 'Client added successfully!')
        return redirect('dashboard_clients')
    return render(request, 'dashboard/portfolio/admin_add_client.html')


# --------- Portfolio Items ---------
@login_required(login_url='login')
def admin_add_portfolio_item(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        PortfolioItem.objects.create(
            item_title=title,
            item_description=description,
            item_image=image
        )
        messages.success(request, 'Portfolio item added successfully!')
        return redirect('admin_portfolio')
    return render(request, 'dashboard/portfolio/admin_add_portfolio_item.html')


@login_required(login_url='login')
def admin_edit_portfolio_item(request, id):
    item = get_object_or_404(PortfolioItem, id=id)
    if request.method == 'POST':
        item.item_title = request.POST.get('title')
        item.item_description = request.POST.get('description')
        if request.FILES.get('image'):
            item.item_image = request.FILES.get('image')
        item.save()
        return redirect('admin_portfolio')
    return render(request, 'dashboard/portfolio/admin_edit_portfolio_item.html', {'item': item})


@login_required(login_url='login')
def admin_delete_portfolio_item(request, id):
    item = get_object_or_404(PortfolioItem, id=id)
    item.delete()
    messages.success(request, 'Portfolio item deleted successfully!')
    return redirect('admin_portfolio')


# --------- Blog Views ---------
@login_required(login_url='login')
def admin_blog_dashboard(request):
    blog_main = Blog.objects.first()
    posts = BlogPost.objects.select_related('author').order_by('-created_at')
    comments = Comment.objects.select_related('post').order_by('-created_at')
    authors = Author.objects.all()
    return render(request, 'dashboard/blog/admin_blog_dashboard.html', {
        'blog_main': blog_main,
        'posts': posts,
        'comments': comments,
        'authors': authors,
    })


@login_required(login_url='login')
def admin_edit_blog_main(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.description = request.POST.get('description')
        if request.FILES.get('image'):
            blog.image = request.FILES.get('image')
        blog.save()
        messages.success(request, "Blog section updated successfully!")
        return redirect('admin_blog_dashboard')
    return render(request, 'dashboard/blog/admin_edit_blog_main.html', {'blog': blog})


@login_required(login_url='login')
def admin_add_blog_post(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        author_id = request.POST.get('author')
        author = Author.objects.get(id=author_id) if author_id else None
        BlogPost.objects.create(
            title=title,
            content=content,
            image=image,
            author=author
        )
        messages.success(request, "Blog post added successfully!")
        return redirect('admin_blog_dashboard')
    return render(request, 'dashboard/blog/admin_add_blog_post.html', {'authors': authors})


@login_required(login_url='login')
def admin_edit_blog_post(request, id):
    post = get_object_or_404(BlogPost, id=id)
    authors = Author.objects.all()
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        author_id = request.POST.get('author')
        post.author = Author.objects.get(id=author_id) if author_id else None
        post.save()
        messages.success(request, "Blog post updated successfully!")
        return redirect('admin_blog_dashboard')
    return render(request, 'dashboard/blog/admin_edit_blog_post.html', {'post': post, 'authors': authors})


@login_required(login_url='login')
def admin_delete_blog_post(request, id):
    post = get_object_or_404(BlogPost, id=id)
    post.delete()
    messages.success(request, "Blog post deleted successfully!")
    return redirect('admin_blog_dashboard')


@login_required(login_url='login')
def admin_delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    messages.success(request, "Comment deleted successfully!")
    return redirect('admin_blog_dashboard')


@login_required(login_url='login')
def admin_add_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        profile_image = request.FILES.get('profile_image')
        Author.objects.create(name=name, bio=bio, profile_image=profile_image)
        messages.success(request, "Author added successfully!")
        return redirect('admin_blog_dashboard')
    return render(request, 'dashboard/blog/admin_add_author.html')


@login_required(login_url='login')
def admin_edit_author(request, id):
    author = get_object_or_404(Author, id=id)
    if request.method == 'POST':
        author.name = request.POST.get('name')
        author.bio = request.POST.get('bio')
        if request.FILES.get('profile_image'):
            author.profile_image = request.FILES.get('profile_image')
        author.save()
        messages.success(request, "Author updated successfully!")
        return redirect('admin_blog_dashboard')
    return render(request, 'dashboard/blog/admin_edit_author.html', {'author': author})


@login_required(login_url='login')
def admin_delete_author(request, id):
    author = get_object_or_404(Author, id=id)
    author.delete()
    messages.success(request, "Author deleted successfully!")
    return redirect('admin_blog_dashboard')



# --- Practice Area Info (edit only) ---
@login_required
def dashboard_practice_area(request):
    # Get the main section (only one)
    main_section = PracticeAreaMain.objects.last()  # latest or only one
    services = PracticeService.objects.all()

    if request.method == 'POST':
        main_section.main_title = request.POST.get('main_title')
        main_section.main_description = request.POST.get('main_description')
        main_section.practice_area = request.POST.get('practice_area')
        main_section.practice_area_description = request.POST.get('practice_area_description')
        if 'main_image' in request.FILES:
            main_section.main_image = request.FILES['main_image']
        main_section.save()
        messages.success(request, "Practice Area section updated successfully.")
        return redirect('dashboard_practice_area')

    return render(request, 'dashboard/practice_area/dashboard_practice_area.html', {
        'practice_area': main_section,
        'services': services,
    })


# --- Edit Service ---
@login_required
def edit_service(request, id):
    service = get_object_or_404(PracticeService, id=id)
    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        if 'icon_image' in request.FILES:
            service.icon_image = request.FILES['icon_image']
        service.save()
        messages.success(request, "Service updated successfully.")
        return redirect('dashboard_practice_area')
    return render(request, 'dashboard/practice_area/edit_service.html', {'service': service})


# --- Delete Service ---
@login_required
def delete_service(request, id):
    service = get_object_or_404(PracticeService, id=id)
    service.delete()
    messages.success(request, "Service deleted successfully.")
    return redirect('dashboard_practice_area')


@login_required
def add_service(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        icon_image = request.FILES.get('icon_image')
        if not name or not description:
            messages.error(request, "Please fill in all required fields.")
            return redirect('add_service')

        PracticeService.objects.create(
            name=name,
            description=description,
            icon_image=icon_image
        )
        messages.success(request, "Service added successfully.")
        return redirect('dashboard_practice_area')

    return render(request, 'dashboard/practice_area/add_service.html')


def dashboard_legal_advice(request):
    legal_messages = FreeLegalAdvice.objects.all().order_by('-submitted_at')
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    
    return render(request, 'dashboard/messages/message.html', {
        'messages': legal_messages,
        'messages_list': contact_messages
    })



def delete_legal_advice(request, pk):
    advice = get_object_or_404(FreeLegalAdvice, pk=pk)
    advice.delete()
    messages.success(request, "Message deleted successfully.")
    return redirect('dashboard_legal_advice')




def admin_organization_settings(request):
    org_info = OrganizationInfo.objects.first()  
    
    if request.method == 'POST':
        if not org_info:
            org_info = OrganizationInfo() 
        
        org_info.name = request.POST.get('name')
        org_info.org_details = request.POST.get('org_details')
        org_info.service_1 = request.POST.get('service_1')
        org_info.service_2 = request.POST.get('service_2')
        org_info.service_3 = request.POST.get('service_3')
        org_info.service_4 = request.POST.get('service_4')
        org_info.service_5 = request.POST.get('service_5')
        org_info.facebook_link = request.POST.get('facebook_link')
        org_info.twitter_link = request.POST.get('twitter_link')
        org_info.linkedin_link = request.POST.get('linkedin_link')
        org_info.instagram_link = request.POST.get('instagram_link')
        
        if 'org_logo' in request.FILES:
            org_info.org_logo = request.FILES['org_logo']
        
        org_info.save()
        messages.success(request, 'Organization info updated successfully!')
        return redirect('admin_organization_settings')
    
    return render(request, 'dashboard/org/org.html', {'org_info': org_info})




def dashboard_attorneys(request):
    attorneys = Attorney.objects.all()
    return render(request, 'dashboard/about/attorney_dashboard.html', {'attorneys': attorneys})


def admin_clients_dashboard(request):
    clients = Client.objects.all().order_by('-id')  # latest first
    return render(request, 'dashboard/clients/clients_dashboard.html', {'clients': clients})




