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
    clients = Client.objects.all()  
    latest_client = Client.objects.last()  

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
        "attorneys_info": attorneys_info,
        "clients": clients,
        "latest_client": latest_client
    })


#main blog view 
def blog_main(request):
    blog = Blog.objects.last()
    blog_content=BlogPost.objects.all()
    context = {
        'blog': blog,
        'blog_content': blog_content
    }

    return render(request, 'ui/blog.html', context)



def blog_single(request, id):
    post = get_object_or_404(BlogPost, id=id)
    comments = post.comments.all().order_by('-created_at')  # fetch comments

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        website = request.POST.get('website')
        message = request.POST.get('message')

        # Create a new comment
        Comment.objects.create(
            post=post,
            name=name,
            email=email,
            website=website,
            message=message
        )
        return redirect('blog_single', id=post.id)  # redirect to refresh page

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'ui/blog-single.html', context)





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
    latest_area = PracticeArea.objects.last() 
    
    if latest_area:
        # Only main section fields
        main_data = {
            'main_title': latest_area.main_title,
            'main_description': latest_area.main_description,
            'main_image': latest_area.main_image,
            'practice_area': latest_area.practice_area,
            'practice_area_description': latest_area.practice_area_description
        }
    else:
        main_data = None

    # Fetch all practice area entries for dynamic display
    all_areas = PracticeArea.objects.all()

    return render(request, 'ui/practice.html', {
        'main': main_data,
        'areas': all_areas
    })
from django.shortcuts import render, get_object_or_404
from .models import PracticeArea

def practice_area_detail(request, id):
    area = get_object_or_404(PracticeArea, id=id)
    areas = PracticeArea.objects.all()  # fetch all practice areas

    context = {
        'area': area,
        'areas': areas  # pass to template for "Other Practice Areas"
    }
    return render(request, 'ui/practice_area_detail.html', context)






def portfolio(request):
    portfolio_main = PortfolioMain.objects.last()
    portfolio_items_list = PortfolioItem.objects.all()

    # Paginate: 6 items per page (change as needed)
    paginator = Paginator(portfolio_items_list, 6)
    page_number = request.GET.get('page')
    portfolio_items = paginator.get_page(page_number)

    context = {
        'portfolio_main': portfolio_main,
        'portfolio_items': portfolio_items
    }
    return render(request, 'ui/won.html', context)

def portfolio_detail(request, id):
    # Get the clicked portfolio item
    item = get_object_or_404(PortfolioItem, id=id)

    # Other portfolio items (Related Cases)
    other_items = PortfolioItem.objects.exclude(id=id)

    context = {
        'item': item,
        'other_items': other_items
    }
    return render(request, 'ui/portfolio_detail.html', context)

