"""Functions for views.py"""
import datetime
import json
import stripe
from django.conf import settings
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, RedirectView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q, Count
from .models import Blog, Categories, Comment, Profile
from .forms import PostForm, myUserCreationForm, myAuthenticationForm, PostComment, ProfileForm, ContactForm
from django.contrib.auth.models import User   

stripe.api_key = settings.STRIPE_SECRET_KEY

class PremiumPageView(TemplateView):
    template_name = 'blog/premium.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def charge(request):
    tmpl = 'blog/charge.html'
    if request.method == 'POST':
        
        current_profile = Profile.objects.get(user=request.user)
        current_profile.premium = True
        current_profile.save()
        
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django Premium charge',
            source=request.POST['stripeToken']
        )
        return render(request, tmpl)

def stats(request):
    tmpl = 'blog/all_stats.html'
    blogs = Blog.objects.filter(author=request.user)
    return render(request, tmpl, {"blogs": blogs})

def likes(request, single_slug): 
    print('Single slug----------------', single_slug)
    obj = get_object_or_404(Blog, blog_slug=single_slug)
    user = request.user
    if user in obj.likes.all():
        obj.likes.remove(user)
        messages.info(request, "Like removed")
    else:
        obj.likes.add(user)
        messages.success(request, "Like added")
    return redirect(f"../{single_slug}")

def contact(request):
    tmpl = "blog/contact.html"
    category = Categories.objects.all()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            from_email = form.cleaned_data.get('from_email')
            message = form.cleaned_data.get('message')
            message = from_email + ' ' + message
            try:
                send_mail(  subject, 
                            message, 
                            from_email,
                            ['nciganovic52@gmail.com'], 
                            fail_silently=False)
                sent = True
            except BadHeaderError:
                messages.error(request, "Failed to send email.")
                sent = False
            if sent == True:
                messages.success(request, "Email sent successfully.")
            return redirect("index")
    else:
        form = ContactForm()
    return render(request, tmpl, {"form": form, 
                                  "category":category})

def change_info(request):
    tmpl = "blog/change_info.html"
    category = Categories.objects.all()
    if request.method == "POST":
        register_form = myUserCreationForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if register_form.is_valid() and profile_form.is_valid():
            is_valid = True
            image = profile_form.cleaned_data.get('image')
            if image:
                w, h = get_image_dimensions(image)
                if w != 100:
                    messages.error(request, "Image width must be 100px")
                    is_valid = False
                    print('Width: ', w)
                if h != 100:
                    messages.error(request, "Image height must be 100px")
                    is_valid = False
            if is_valid == True:
                register_form.save()
                profile_form.save()
                username = register_form.cleaned_data.get('username')
                raw_password = register_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                messages.success(request, f"Information successfully changed!")
                return redirect("my_info")
        else:
            messages.error(request, f"Information not changed successfully!")
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        register_form = myUserCreationForm(instance=request.user)
    return render(request, tmpl, context={"register":register_form,
                                          "profile":profile_form,
                                          "category": category,})

def my_info(request):
    tmpl = "blog/my_info.html"
    profile = Profile.objects.filter(user=request.user)
    user_blogs = Blog.objects.filter(author=request.user)
    views_sum = 0
    likes_sum = 0
    
    for blog in user_blogs: 
        print('--------------------------')
        print('Name---', blog.headline)
        print('View---', blog.views.count())
        print('Likes---', blog.likes.count())
        views_sum += blog.views.count()
        likes_sum += blog.likes.count()
        print('--------------------------')
        print('View sum-->',blog.headline, ' ', views_sum)
        print('Likes sum-->',blog.headline, ' ', likes_sum)
        print('--------------------------')
    
    comments_on_user_blog = Blog.objects.filter()

    category = Categories.objects.all()
    return render(request, tmpl, context={"profile": profile, 
                                          "category": category,
                                          "views_sum":json.dumps(views_sum),
                                          "likes_sum": json.dumps(likes_sum),})

def my_blogs(request):
    tmpl = "blog/my_blogs.html"
    current_author = request.user
    blogs = Blog.objects.filter(author=current_author)
    category = Categories.objects.all()
    return render(request, tmpl, context={"blogs": blogs, 
                                          "category": category})

def delete_blog(request, single_slug):
    current_author = request.user
    blogs_author = [b.blog_slug for b in Blog.objects.filter(author=current_author)] 
    if single_slug in blogs_author:
        matching_blog = Blog.objects.get(blog_slug=single_slug)
    if request.method == "POST":
        category = Categories.objects.all()
        matching_blog.delete()
        messages.success(request, f"Blog successfully deleted!")
        return redirect("my_blogs")
    else:
        category = Categories.objects.all()
        current_author = request.user
        blogs_author = [b.blog_slug for b in Blog.objects.filter(author=current_author)] 
        if single_slug in blogs_author:
            matching_blog = Blog.objects.get(blog_slug=single_slug)
            return render(request, 'blog/delete_blog.html', context={"delete_blog": matching_blog, "category":category})

def edit_blog(request, single_slug):
    tmpl = "blog/edit_blog.html"
    fixed = False
    current_author = request.user
    blogs_author = [b.blog_slug for b in Blog.objects.filter(author=current_author)] 
    if single_slug in blogs_author:
        matching_blog = Blog.objects.get(blog_slug=single_slug)
    if request.method == "POST":
        category = Categories.objects.all()
        form = PostForm(request.POST, request.FILES, instance=matching_blog)
        if form.is_valid():
            is_valid = True
            image = form.cleaned_data.get('image')
            if image.size > 1024*1024:
                messages.error(request, 'Image is larger then 1MB')
                is_valid = False
            w, h = get_image_dimensions(image)
            if w != 600:
                messages.error(request, "Image width must be 600px")
                is_valid = False
            if h != 400:
                messages.error(request, "Image height must be 400px")
                is_valid = False
            if is_valid == True:
                edited_form = form.save(commit=False)
                edited_form.author = request.user
                edited_form.save()
                messages.success(request, "Blog successfully changed!")
                return redirect("my_blogs")
            else:
                return redirect(f"../my_blogs/{matching_blog.blog_slug}")
        else:
            form = PostForm(instance=matching_blog)
            messages.error(request, "Blog not changed!")
    else:
        category = Categories.objects.all()
        current_author = request.user
        blogs_author = [b.blog_slug for b in Blog.objects.filter(author=current_author)] 
        if single_slug in blogs_author:
            matching_blog = Blog.objects.get(blog_slug=single_slug)
            form = PostForm(instance=matching_blog)
            return render(request, tmpl, context={"edit_blog": matching_blog, 
                                                  "form": form, 
                                                  "category": category,
                                                  "fixed": fixed})

def create_blog(request):
    """Creating User's Blog"""
    tmpl = "blog/create_blog.html"
    fixed = False
    if request.method == "POST":
        blog_post_form = PostForm(request.POST, request.FILES)
        category = Categories.objects.all()
        if blog_post_form.is_valid():
            is_valid = True
            image = blog_post_form.cleaned_data.get('image')
            if image.size > 1024*1024:
                messages.error(request, "Image is larger then 1MB")
                is_valid = False
            w, h = get_image_dimensions(image)
            if w != 600:
                messages.error(request, "Image width must be 600px")
                is_valid = False
            if h != 400:
                messages.error(request, "Image height must be 400px")
                is_valid = False
            if is_valid == True:
                form = blog_post_form.save(commit=False)
                form.author = request.user
                form.save()
                messages.success(request, "Blog successfully created!")
                return redirect("index")
        else:
            messages.error(request, "You need to fill all the fields!")
    else:
        blog_post_form = PostForm()
        category = Categories.objects.all()
    return render(request, tmpl, context={"form": blog_post_form,
                                          "category":category,
                                          "fixed": fixed})

def single_slug(request, single_slug):
    """Creating links for every category"""
    category = Categories.objects.all()
    categories = [c.category_slug for c in Categories.objects.all()] 
    if single_slug in categories:
        tmpl = "blog/blog_titles.html"
        matching_blogs = Blog.objects.filter(category_name__category_slug=single_slug)[2:]
        first_two_matching_blogs = Blog.objects.filter(category_name__category_slug=single_slug)[0:2]
        this_category = Categories.objects.get(category_slug=single_slug)
        most_viewed = Blog.objects.filter(category_name__category_slug=single_slug).annotate(v_count=Count('views')).order_by('-v_count')[:5]
        return render(request, tmpl, context={"blogs": matching_blogs, 
                                              "category":category, 
                                              "first_two_matching_blogs": first_two_matching_blogs,
                                              "this_category": this_category,
                                              "most_viewed": most_viewed})
    blogs = [b.blog_slug for b in Blog.objects.all()] 
    if single_slug in blogs:
        user = request.user
        tmpl = 'blog/blog.html'
        matching_blog = Blog.objects.get(blog_slug=single_slug)
        comments = Comment.objects.filter(blog=matching_blog).order_by('-id')
        if request.method == "POST": 
            comment_form = PostComment(request.POST or None)
            if comment_form.is_valid():
                content = request.POST.get('comment_text')
                comment = Comment.objects.create(blog=matching_blog, author=user, comment_text=content)
                comment.save()
                return HttpResponseRedirect(request.path_info)
        else:
            comment_form = PostComment()
            category = Categories.objects.all()
            if user.is_authenticated:
                if matching_blog.author != user:
                    print('------Blog author: ',matching_blog.author)
                    print('------Current user: ',user)
                    matching_blog.views.add(user)

            if user in matching_blog.likes.all():
                like_value = 'Dislike'
            else:
                like_value = 'Like'
        context = {
            "single_blog": matching_blog, 
            "comments":comments,
            "comment_form":comment_form,
            "category":category,
            "like_value":like_value,
        }
        return render(request, tmpl, context)   

def logout_request(request):
    """Logging out"""
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("index")

def login_request(request):
    """Logging in"""
    category = Categories.objects.all()
    if request.method == "POST":
        form = myAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("index")
            else: messages.error(request, "Invalid username or password")
        else: messages.error(request, "Invalid username or password")
    else:
        form = myAuthenticationForm()
    return render(request, "blog/login.html", {"form": form, 'category':category})

def register(request):
    """Registering new user"""
    category = Categories.objects.all()
    if request.method == 'POST':
        form = myUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f"{username} created account!")
            return redirect('/')
        else:
            messages.error(request, "Registration failed, please try again.")
    else:
        form = myUserCreationForm()
        profile_form = ProfileForm()
    return render(request, "blog/register.html", {"form": form, 
                                                  "category":category})

def index(request):
    """Loading index page"""
    tmpl = "blog/index.html"
    search = False
    category = Categories.objects.all()
    blogs = Blog.objects.all()
    most_recent = Blog.objects.all().order_by('-id')[:5]
    
    most_liked = Blog.objects.annotate(l_count=Count('likes')).order_by('-l_count')[:5]
    for ml in most_liked:
        print('Number of likes ------>', ml.likes.count(), 'Headline of blog ------>', ml.headline)
    
    premium_user = User.objects.filter(profile__premium = True)
    print('First premium user: ',premium_user[0])

    single_premium_blog = []
    for i in range(5):
        premium_blog = Blog.objects.filter(author=premium_user[i]).order_by('views')[:1]
        single_premium_blog.append(premium_blog[0])
        print(i, '- Single_premium_blog:',single_premium_blog[i])
  
    print('--------->',single_premium_blog[0])
    print('--------->',single_premium_blog[1])
    print('--------->',single_premium_blog[2])
    print('--------->',single_premium_blog[3])
    print('--------->',single_premium_blog[4])

    '''
    for blog in blogs:
        print(blog.content.split()[14:30])
        break
    '''
    query = request.GET.get('q'); 
    if query:
        search = True
        blogs = blogs.filter(
            Q(headline__icontains=query) |
            Q(content__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) 
        ).distinct()
        if not blogs:
            messages.error(request, f"Search {query} doesnt exist")
    return render(request, tmpl, context={"category": category, 
                                          "search": search, 
                                          "blogs": blogs,
                                          "most_recent": most_recent,
                                          "most_liked": most_liked,
                                          "query": query,
                                          "single_premium_blog_1":single_premium_blog[0],
                                          "single_premium_blog_2":single_premium_blog[1],
                                          "single_premium_blog_3":single_premium_blog[2],
                                          "single_premium_blog_4":single_premium_blog[3],
                                          "single_premium_blog_5":single_premium_blog[4],})
