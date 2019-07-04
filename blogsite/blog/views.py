from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import Blog, Categories
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import PostForm

def create_blog(request):
    categ_select = Categories.objects.all
    if request.method == 'POST':
        blog_post_form = PostForm(request.POST)
        print("------BLOG POST ERROR--------")
        print(blog_post_form.errors)
        print("------BLOG POST ERROR--------")
        if blog_post_form.is_valid():
            print("---------------------VALID FORM-------------------------")
            
            headline = blog_post_form.cleaned_data.get('headline')
            category_name = blog_post_form.cleaned_data.get('category_name')
            content = blog_post_form.cleaned_data.get('content')
            blog_slug = blog_post_form.cleaned_data.get('blog_slug')
            
            blog_post_form.save()
            
            return redirect("index")
    else: 
        blog_post_form = PostForm()
        
    return render(request, 
                 "blog/create_blog.html",
                 context={"form": blog_post_form , "categories": categ_select })


def single_slug(request, single_slug):
    categories = [c.category_slug for c in Categories.objects.all()] 
    if single_slug in categories:
        matching_categories = Blog.objects.filter(category_name__category_slug = single_slug)
        return render(request=request,
                      template_name='blog/blog_titles.html',
                      context={"blogs": matching_categories})

    blogs = [b.blog_slug for b in Blog.objects.all()] 
    if single_slug in blogs:
        matching_blog = Blog.objects.get(blog_slug = single_slug)
        return render(request,
                      'blog/blog.html',
                       context={"single_blog": matching_blog})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect("index")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("index")
            else: 
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request, 
                 "blog/login.html",
                 {"form": form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def index(request):
    category =  Categories.objects.all
    return render(request, 
                  'blog/index.html',
                 context={"category": category})


