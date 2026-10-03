from django.db import models


from companies.models import Company


class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Job(models.Model):

    JOB_TYPE_CHOICES = (
    ('full_time', 'Full Time'),
    ('part_time', 'Part Time'),
    ('internship', 'Internship'),
    ('contract', 'Contract'),
    ('remote', 'Remote'),
    ('hybrid', 'Hybrid'),
)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=150
    )

    description = models.TextField()

    location = models.CharField(
        max_length=100
    )

    salary_min = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    salary_max = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    experience = models.PositiveIntegerField(
        default=0
    )

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPE_CHOICES
    )

    skills = models.TextField()

    deadline = models.DateField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title
