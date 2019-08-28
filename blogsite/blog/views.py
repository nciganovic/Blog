"""Functions for views.py"""
import datetime
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from .models import Blog, Categories, Comment, Profile
from .forms import PostForm, myUserCreationForm, myAuthenticationForm, PostComment, ProfileForm, ContactForm
from django.contrib.auth.models import User   

def contact(request):
    tmpl = 'blog/contact.html'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            from_email = form.cleaned_data.get('from_email')
            message = form.cleaned_data.get('message')
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
                sent = True
            except BadHeaderError:
                messages.error(request, "Failed to send email.")
                sent = False
            if sent == True:
                messages.success(request, "Email sent successfully.")
            return redirect("index")
    else:
        form = ContactForm()
    return render(request, tmpl, {"form": form})


def change_info(request):
    tmpl = 'blog/change_info.html'
    if request.method == 'POST':
        register_form = myUserCreationForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if register_form.is_valid():
            register_form.save()
            profile_form.save()

            username = register_form.cleaned_data.get('username')
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f"Information successfuly changed!")
            return redirect("my_info")
        else:
            messages.error(request, f"Information not changed successfuly!")
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        register_form = myUserCreationForm(instance=request.user)
        
    return render(request, tmpl, context={
            "register":register_form,
            "profile":profile_form,
    })

def my_info(request):
    tmpl = 'blog/my_info.html'
    profile = Profile.objects.filter(user=request.user)
    return render(request, tmpl, context={"profile": profile})

def my_blogs(request):
    tmpl = "blog/my_blogs.html"
    current_author = request.user
    blogs = Blog.objects.filter(author = current_author)
    
    return render(request, tmpl, context={"blogs": blogs })

def delete_blog(request, single_slug):
    current_author = request.user
    blogs_author = [b.blog_slug for b in Blog.objects.filter(author=current_author)] 
    if single_slug in blogs_author:
        matching_blog = Blog.objects.get(blog_slug=single_slug)
    if request.method == 'POST':
        matching_blog.delete()
        messages.success(request, f"Blog successfully deleted!")
        return redirect("my_blogs")
    else:
        current_author = request.user
        blogs_author = [b.blog_slug for b in Blog.objects.filter(author=current_author)] 
        if single_slug in blogs_author:
            matching_blog = Blog.objects.get(blog_slug=single_slug)
            return render(request, 'blog/delete_blog.html', context={"delete_blog": matching_blog })

def edit_blog(request, single_slug):
    current_author = request.user
    blogs_author = [b.blog_slug for b in Blog.objects.filter(author=current_author)] 
    if single_slug in blogs_author:
        matching_blog = Blog.objects.get(blog_slug=single_slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=matching_blog)
        if form.is_valid():
            edited_form = form.save(commit=False)
            edited_form.author = request.user
            edited_form.save()
            messages.success(request, f"Blog successfully changed!")
            return redirect("my_blogs")
        else:
            form = PostForm(instance=matching_blog)
            messages.error(request, f"Blog not changed!")
    else:
        current_author = request.user
        blogs_author = [b.blog_slug for b in Blog.objects.filter(author=current_author)] 
        if single_slug in blogs_author:
            matching_blog = Blog.objects.get(blog_slug=single_slug)
            form = PostForm(instance=matching_blog)
            return render(request, 'blog/edit_blog.html', context={"edit_blog": matching_blog , "form": form})

def create_blog(request):
    """Creating User's Blog"""
    tmpl = "blog/create_blog.html"
    if request.method == 'POST':
        blog_post_form = PostForm(request.POST, request.FILES)
        #print(blog_post_form.errors)
        if blog_post_form.is_valid():
            form = blog_post_form.save(commit=False)
            form.author = request.user
            form.save()
            messages.success(request, f"Blog successfully created!")
            return redirect("index")
        else:
            messages.error(request, f"You need to fill all the fields!")
    else:
        blog_post_form = PostForm()
    return render(request, tmpl, context={"form": blog_post_form })


def single_slug(request, single_slug):
    """Creating links for every category"""
    categories = [c.category_slug for c in Categories.objects.all()] 
    if single_slug in categories:
        matching_categories = Blog.objects.filter(category_name__category_slug=single_slug)
        return render(request=request,
                      template_name='blog/blog_titles.html',
                      context={"blogs": matching_categories})
    blogs = [b.blog_slug for b in Blog.objects.all()] 
    if single_slug in blogs:
        matching_blog = Blog.objects.get(blog_slug=single_slug)
        comments = Comment.objects.filter(blog=matching_blog).order_by('-id')
        if request.method == 'POST': 
            comment_form = PostComment(request.POST or None)
            if comment_form.is_valid():
                content = request.POST.get('comment_text')
                comment = Comment.objects.create(blog=matching_blog, author=request.user, comment_text=content)
                comment.save()
                return HttpResponseRedirect(request.path_info)
        else:
            comment_form = PostComment()
        context = {
            "single_blog": matching_blog, 
            "comments":comments,
            "comment_form":comment_form,
        }
        return render(request, 'blog/blog.html', context)   

def logout_request(request):
    """Logging out"""
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("index")

def login_request(request):
    """Logging in"""
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

    form = myAuthenticationForm()
    return render(request, "blog/login.html", {"form": form})

def register(request):
    """Registering new user"""
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
    return render(request, 'blog/register.html', {'form': form})

def index(request):
    """Loading index page"""
    search = False
    category = Categories.objects.all()
    blogs = Blog.objects.all()
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
    return render(request, 'blog/index.html', context={"category": category, "search": search, "blogs": blogs})
