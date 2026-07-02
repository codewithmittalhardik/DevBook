from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    # Extra developer metadata fields
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        help_text="Tell your classmates or colleagues about your background."
    )
    linkedin_url = models.URLField(
        blank=True, 
        null=True, 
        help_text="Link to your professional LinkedIn profile."
    )

    def __str__(self):
        return f"Profile for {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=100)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200, help_text="Comma-separated tags (e.g. Django, MySQL, JS)")
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        if not self.tech_stack:
            return []
        return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]

    @property
    def github_url_display(self):
        if self.github_link:
            return self.github_link
        github_account = self.user.socialaccount_set.filter(provider='github').first()
        if github_account:
            return github_account.extra_data.get('html_url') or f"https://github.com/{github_account.extra_data.get('login')}"
        return None

    @property
    def github_username_display(self):
        github_account = self.user.socialaccount_set.filter(provider='github').first()
        if github_account:
            return github_account.extra_data.get('login')
        return None

from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('project', 'user')

    def __str__(self):
        return f"Review ({self.rating} stars) for {self.project.title} by {self.user.username}"