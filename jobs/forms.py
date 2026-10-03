from django import forms
from django.utils import timezone

from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = (
            'category',
            'title',
            'description',
            'location',
            'salary_min',
            'salary_max',
            'experience',
            'job_type',
            'skills',
            'deadline',
            'is_active',
        )

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Python Django Developer',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': (
                        'Describe the role, responsibilities, '
                        'requirements and expectations...'
                    ),
                    'rows': 7,
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Pune, Maharashtra',
                }
            ),

            'salary_min': forms.NumberInput(
                attrs={
                    'placeholder': 'e.g. 300000',
                    'min': 0,
                }
            ),

            'salary_max': forms.NumberInput(
                attrs={
                    'placeholder': 'e.g. 600000',
                    'min': 0,
                }
            ),

            'experience': forms.NumberInput(
                attrs={
                    'placeholder': 'e.g. 2',
                    'min': 0,
                }
            ),

            'skills': forms.Textarea(
                attrs={
                    'placeholder': (
                        'e.g. Python, Django, SQL, REST API'
                    ),
                    'rows': 4,
                }
            ),

            'deadline': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title and not title.strip():
            raise forms.ValidationError(
                'Job title cannot be empty.'
            )

        return title.strip() if title else title

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if description and not description.strip():
            raise forms.ValidationError(
                'Job description cannot be empty.'
            )

        return description.strip() if description else description

    def clean_salary_min(self):
        salary_min = self.cleaned_data.get('salary_min')

        if salary_min is not None and salary_min < 0:
            raise forms.ValidationError(
                'Minimum salary cannot be negative.'
            )

        return salary_min

    def clean_salary_max(self):
        salary_max = self.cleaned_data.get('salary_max')

        if salary_max is not None and salary_max < 0:
            raise forms.ValidationError(
                'Maximum salary cannot be negative.'
            )

        return salary_max

    def clean(self):
        cleaned_data = super().clean()

        salary_min = cleaned_data.get('salary_min')
        salary_max = cleaned_data.get('salary_max')
        deadline = cleaned_data.get('deadline')

        # Check salary range
        if (
            salary_min is not None
            and salary_max is not None
            and salary_min > salary_max
        ):
            raise forms.ValidationError(
                'Minimum salary cannot be greater than maximum salary.'
            )

        # Check deadline
        if deadline and deadline < timezone.localdate():
            raise forms.ValidationError(
                'Job deadline cannot be in the past.'
            )

        return cleaned_data