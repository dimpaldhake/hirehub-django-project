from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application

        fields = (
            'resume',
            'cover_letter',
        )

    def clean_resume(self):

        resume = self.cleaned_data.get('resume')

        if resume:

            allowed_extensions = [
                '.pdf',
                '.doc',
                '.docx'
            ]

            extension = resume.name.lower()

            if not extension.endswith(
                tuple(allowed_extensions)
            ):
                raise forms.ValidationError(
                    'Only PDF, DOC, and DOCX files are allowed.'
                )

        return resume