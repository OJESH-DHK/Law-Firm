from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *



#index page view
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (
    Index, PracticeAreaMain, PracticeService, Client,
    Blog, BlogPost, Attorney, AboutUs,
    FreeLegalAdvice, LegalAdviceInfo
)

def index(request):
    index_sections = Index.objects.all()
    latest_area = PracticeAreaMain.objects.last()
    practice_area = PracticeService.objects.all()[:3]  # Only get first 3 areas
    clients = Client.objects.all()
    blog = Blog.objects.last()
    blog_posts_list = BlogPost.objects.all().order_by('-created_at')
    latest_client = Client.objects.last()
    attorneys = Attorney.objects.all()
    latest_info = AboutUs.objects.last()
    legal_info = LegalAdviceInfo.objects.last()  # background image for Free Legal Advice section

    # ✅ Handle form submission
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        FreeLegalAdvice.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(request, "✅ Your message has been sent successfully!")
        return redirect('index')  # reload home page after submission

    context = {
        'index_sections': index_sections,
        'main': latest_area,
        'areas': practice_area,
        'clients': clients,
        'latest_info': latest_info,
        'blog': blog,
        'blog_content': blog_posts_list[:3],
        'attorneys': attorneys, 
        'latest_client': latest_client,
        'legal_info': legal_info,  # send background image info
    }

    return render(request, 'ui/index.html', context)



def about(request):
    latest_info = AboutUs.objects.last()
    clients = Client.objects.all()
    latest_client = Client.objects.last()
    attorneys = Attorney.objects.all()  # ✅ Now using Attorney model

    return render(request, 'ui/about.html', {
        "latest_info": latest_info,
        "attorneys": attorneys,
        "clients": clients,
        "latest_client": latest_client,
    })





#main blog view 

def blog_main(request):
    blog = Blog.objects.last()
    blog_posts_list = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(blog_posts_list, 6)
    page_number = request.GET.get('page')
    blog_content = paginator.get_page(page_number)

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
        return redirect('blog_single', id=post.id) 


    related_blogs = BlogPost.objects.exclude(id=post.id).order_by('-created_at')[:3]

    recent_blogs = BlogPost.objects.exclude(id=post.id).order_by('-created_at')[:3]

    context = {
        'post': post,
        'comments': comments,
        'related_blogs': related_blogs,
        'recent_blogs': recent_blogs
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

    gallery = Gallery.objects.last()

    all_images = GalleryImage.objects.filter(gallery=gallery).order_by('-id')
    

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


from django.core.paginator import Paginator

def practice(request):
    latest_area = PracticeAreaMain.objects.last() 
    practice_area = PracticeService.objects.all()
    context = {
        'main': latest_area,
        'areas': practice_area,
    }

    return render(request, 'ui/practice.html', context)



def practice_area_detail(request, id):
    # Get the requested service
    area = get_object_or_404(PracticeService, id=id)
    
    # Get 3 other services excluding the current one
    other_areas = PracticeService.objects.exclude(id=area.id).order_by('-id')[:3]

    context = {
        'area': area,
        'other_areas': other_areas,
    }
    return render(request, 'ui/practice_area_detail.html', context)







def portfolio(request):
    portfolio_main = PortfolioMain.objects.last()
    portfolio_items_list = PortfolioItem.objects.all()
    clients = Client.objects.all() 


    paginator = Paginator(portfolio_items_list, 6)
    page_number = request.GET.get('page')
    portfolio_items = paginator.get_page(page_number)

    context = {
        'portfolio_main': portfolio_main,
        'portfolio_items': portfolio_items,
        'clients': clients
    }
    return render(request, 'ui/won.html', context)

def portfolio_detail(request, id):

    item = get_object_or_404(PortfolioItem, id=id)


    other_items = PortfolioItem.objects.exclude(id=id)

    context = {
        'item': item,
        'other_items': other_items
    }
    return render(request, 'ui/portfolio_detail.html', context)

