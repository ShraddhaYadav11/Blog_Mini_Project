
from tokenize import group
from unicodedata import name
from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import post
from django.contrib.auth.models import Group
# Create your views here.
# home


def home(request):
    posts=post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})
# about


def about(request):
    return render(request, 'blog/about.html')

# contact


def contact(request):
    return render(request, 'blog/contact.html')

# dashboard


def dashboard(request):
    #if request.user.is_authenticated:
     posts=post.objects.all()
     
     return render(request, 'blog/dashboard.html',{'posts':posts})
    #else:
     #return HttpResponseRedirect('/login/')
# Login


def user_login(request):
   
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in successfully !!')
                    return HttpResponseRedirect('/dash/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    


 
# signup
def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations , you have signup successfully!!')
            user=form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)

    else:

        form = SignupForm()
    return render(request, 'blog/signup.html', {'form': form})

# logout


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#add post

def add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                Desc = form.cleaned_data['Desc']
                pst=post(title=title,Desc=Desc)
                pst.save()
                form=PostForm()
        else:
            form=PostForm()
        return render(request, 'blog/add.html',{'form':form})
    else:
       return HttpResponseRedirect('/login/')

#edit post
 
def update_info(request,id):
    if request.method=='POST':
        pi=post.objects.get(pk=id)
        fm=PostForm(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi=post.objects.get(pk=id)
        fm=PostForm(instance=pi)
    return render(request, 'blog/update.html',{'form':fm})

  #delete post
        
def delete(request,id):
    if request.user.is_authenticated:
        if request.method=='POST':
         pi=post.objects.get(pk=id)
         pi.delete()   
        
        return HttpResponseRedirect('/dash/')
    else:
       return HttpResponseRedirect('/login/')

