from django import forms
from django.contrib.auth.models import User
from allauth.socialaccount.forms import SignupForm
from .models import Profile, Project

# 1. USER REGISTRATION FORM
class SocialSignupForm(SignupForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username'
        }),
        help_text='This username will be used for your DevBook profile.'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('Please enter a username.')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def save(self, request):
        user = super().save(request)
        user.username = self.cleaned_data['username']
        user.save(update_fields=['username'])
        return user


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose a strong password'
    }))
    
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Repeat password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
        }

    # Custom clean method to make sure both passwords match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


# 2. USER PROFILE UPDATE FORM
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'linkedin_url']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about your tech journey...'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
        }


# 3. PROJECT SUBMISSION FORM (CRUD)
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        # We explicitly skip 'user' because we attach the logged-in user automatically in views.py
        fields = ['title', 'description', 'tech_stack', 'github_link', 'live_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'What features did you build?'}),
            'tech_stack': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Django, MySQL, JavaScript'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'GitHub Repo Link'}),
            'live_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Live Deployment Link (Optional)'}),
        }