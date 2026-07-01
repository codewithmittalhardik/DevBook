from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied

from .models import Project, Profile
from .forms import SignUpForm, ProjectForm, ProfileForm

# ==================== PUBLIC/DASHBOARD VIEWS ====================

def dashboard(request):
    """Displays the landing page / homepage with a centered welcome banner."""
    return render(request, 'projects/dashboard.html')


def projects_list(request):
    """
    Displays the global registry: all project cards from all users.
    Includes the dataset that JavaScript will use for real-time filtering.
    """
    projects = Project.objects.all().select_related('user', 'user__profile')
    return render(request, 'projects/projects_list.html', {'projects': projects})


def about_project(request):
    """Renders the About DevBook overview page describing platform features."""
    return render(request, 'projects/about.html')


# ==================== AUTHENTICATION VIEWS ====================

def signup_view(request):
    """Handles new account creation and securely hashes passwords."""
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user (Password hashing happens automatically here)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Log the user in immediately after successful signup
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'projects/signup.html', {'form': form})


def login_view(request):
    """Handles secure user sessions."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'projects/login.html', {'form': form})


def logout_view(request):
    """Destroys the user session."""
    if request.method == 'POST':
        logout(request)
    return redirect('dashboard')


# ==================== PROJECT CRUD VIEWS ====================

@login_required
def project_create(request):
    """Allows authenticated users to register a new programming project."""
    github_account = request.user.socialaccount_set.filter(provider='github').first()
    github_username = github_account.extra_data.get('login') if github_account else None
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            # Row-Level Security: Automatically bind the project to the logged-in user
            project.user = request.user
            project.save()
            return redirect('dashboard')
    else:
        initial_data = {}
        if github_account:
            github_url = github_account.extra_data.get('html_url') or f"https://github.com/{github_username}"
            initial_data['github_link'] = github_url
        form = ProjectForm(initial=initial_data)
    return render(request, 'projects/project_form.html', {
        'form': form, 
        'action': 'Add New',
        'github_username': github_username
    })


@login_required
def project_update(request, pk):
    """Allows owners to modify their own project profiles."""
    project = get_object_or_404(Project, pk=pk)
    
    # Strict Authorization Boundary Check
    if project.user != request.user:
        raise PermissionDenied("You do not have permission to edit this project.")
        
    github_account = request.user.socialaccount_set.filter(provider='github').first()
    github_username = github_account.extra_data.get('login') if github_account else None

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {
        'form': form, 
        'action': 'Edit',
        'github_username': github_username
    })


@login_required
def project_delete(request, pk):
    """Allows owners to delete their project profiles."""
    project = get_object_or_404(Project, pk=pk)
    
    # Strict Authorization Boundary Check
    if project.user != request.user:
        raise PermissionDenied("You do not have permission to delete this project.")

    if request.method == 'POST':
        project.delete()
        return redirect('dashboard')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})


# ==================== USER PROFILE VIEW ====================

@login_required
def profile_edit(request):
    """Allows users to update their developer bio, certificate links, and LinkedIn."""
    # Fetch or create the profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'projects/profile_form.html', {'form': form})


@login_required
def profile_delete(request):
    """Allows users to permanently delete their own account and related data."""
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        return redirect('dashboard')
    return render(request, 'projects/profile_confirm_delete.html', {'user': request.user})