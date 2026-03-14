from os import name
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import CustomUser
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CustomUser


def homepage1(request):
    return render(request, 'homepage1.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")
        role = request.POST.get("role")
        level = request.POST.get("level")
        degree = request.POST.get("degree")
        branch = request.POST.get("branch")
        experience = request.POST.get("experience")

        # Password match check
        if password != repassword:
            messages.error(request, "Passwords do not match")
            return redirect("users:signup")

        # Duplicate email check
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("users:login")

        # Create user - FIXED: removed username kwarg, added name
        user = CustomUser.objects.create_user(
            email=email,      # First positional arg = USERNAME_FIELD
            password=password,
            name=name,        # Your custom field
            role=role
        )

        # Optional: Save extra data if student
        if role == "student":
            user.level = level
            user.degree = degree
            user.branch = branch

        # Optional: Save extra data if working
        if role == "working":
            user.experience = experience

        user.save()
        return redirect("users:login")

    return render(request, "signup.html")


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def homepage(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    return render(request, 'homepage.html')  # Your main homepage after login

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:homepage')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


# your_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import re
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.db import connection


from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.contrib import messages

def forgotpassword_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('reNewPassword')
        
        # Email validation first
        if not email:
            messages.error(request, 'Please enter your email address')
            return render(request, 'forgotpassword.html')
            
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            messages.error(request, 'Invalid email format')
            return render(request, 'forgotpassword.html')
        
        # Check user exists (use ORM)
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'Email not found')
            return render(request, 'forgotpassword.html')
        
        # Password validation
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'forgotpassword.html')
            
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters')
            return render(request, 'forgotpassword.html')
        
        # Secure update with transaction
        user.set_password(new_password)  # Better than make_password()
        user.save()
        messages.success(request, 'Password updated successfully!')
        return redirect('users:login')
    
    return render(request, 'forgotpassword.html')



from django.shortcuts import render

def domain(request):

    if request.method == "POST":

        domain = request.POST.get("domain")
        level = request.POST.get("level")

        user = request.user
        user.selected_domain = domain
        user.selected_level = level
        user.save()

        return redirect("users:projects")

    return render(request, "domainselection.html")


from .models import Project

def projects(request):
    domain = request.GET.get('domain')
    level = request.GET.get('level')

    projects = Project.objects.all()

    if domain:
        projects = projects.filter(domain=domain)

    if level:
        projects = projects.filter(level=level)

    return render(request, 'projects.html', {'projects': projects})


from .models import Bookmark, Project
from django.shortcuts import redirect
def bookmark(request, project_id):
    project= get_object_or_404(Project, id=project_id)
    if request.user in project.bookmarked_by.all():
        project.bookmarked_by.remove(request.user)
    else:
        project.bookmarked_by.add(request.user)
    return redirect('users:project.html', project_id=project_id)


def feedback(request):
    return render(request,"feedback.html")


from django.contrib.auth.decorators import login_required

@login_required

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('users:login')   # ✅ correct

    projects = Project.objects.all()  # safer unless Project has user FK
    return render(request, "dashboard.html", {'projects': projects})


def projectdetail(request):
    return render(request,"projectdetail.html")
from django.shortcuts import render
from .models import Bookmark
from django.contrib.auth.decorators import login_required

@login_required
def bookmark_page(request):
    bookmarks = Bookmark.objects.filter(user=request.user)

    return render(request, "bookmarks.html", {
        "bookmarks": bookmarks
    })
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Project, Bookmark
from django.contrib.auth.decorators import login_required

@login_required
def bookmark_project(request, project_id):

    if request.method == "POST":

        project = get_object_or_404(Project, id=project_id)

        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            project=project
        )

        if created:
            return JsonResponse({"status": "saved"})
        else:
            return JsonResponse({"status": "already_saved"})

def logout_view(request):
    logout(request)
    return redirect('users:homepage1')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chatbot(request):

    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message","").lower()

        response = "Sorry, I didn't understand."

        if "hello" in message:
            response = "Hello! How can I help you?"
        elif "project" in message:
            response = "You can explore projects based on domain and difficulty."
        elif "data science" in message:
            response = "There are many Data Science projects like prediction models."

        return JsonResponse({"response": response})

    return JsonResponse({"response": "Invalid request"})