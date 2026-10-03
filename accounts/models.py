from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPE_CHOICES =(
        ('job_seeker','Job Seeker'),
        ('recruiter','Recruiter'),
    )

    user = models.OneToOneField(User ,on_delete=models.CASCADE)

    phone = models.CharField(max_length=15,blank=True)
    location=models.CharField(max_length=100,blank=True)
    skills = models.TextField(blank=True)
    experience=models.PositiveIntegerField(default=0)

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    Profile_picture = models.ImageField(
        upload_to='profile_pictures',
        blank=True,
        null=True
    )

    user_type=models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES
    )

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
