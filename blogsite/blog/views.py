"""Functions for views.py"""
import datetime
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from .models import Blog, Categories, Comment, Profile
from .forms import PostForm, myUserCreationForm, myAuthenticationForm, PostComment
from django.contrib.auth.models import User   

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
            return redirect("my_blogs")
        else:
            form = PostForm(instance=matching_blog)
        
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
        #print("------BLOG POST ERROR--------")
        #print(blog_post_form.errors)
        #print("------BLOG POST ERROR--------")
        if blog_post_form.is_valid():
            #print("---------------------VALID FORM-------------------------")
            form = blog_post_form.save(commit=False)
            form.author = request.user
            form.save()

            return redirect("index")
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
            return redirect('/')
    else:
        form = myUserCreationForm()
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
    return render(request, 'blog/index.html', context={"category": category, "search": search, "blogs": blogs})
