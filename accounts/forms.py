from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    user_type = forms.ChoiceField(
        choices=Profile.USER_TYPE_CHOICES,
        required=True
    )

    class Meta:
        model = User
        fields =(
            'username',
            'email',
            'user_type',
            'password1',
            'password2'
        )

    def clean_email(self):
        email=self.cleaned_data['email'].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registerd."
            )
        return email
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = (
            'phone',
            'location',
            'skills',
            'experience',
            'resume'
        )

        widgets = {

            'phone': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your phone number'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Pune, Maharashtra'
                }
            ),

            'skills': forms.Textarea(
                attrs={
                    'placeholder': 'Python, Django, SQL, React',
                    'rows': 4
                }
            ),

            'experience': forms.NumberInput(
                attrs={
                    'placeholder': 'Years of experience',
                    'min': 0
                }
            ),

            'resume': forms.ClearableFileInput(
                attrs={
                    'accept': '.pdf,.doc,.docx'
                }
            ),
        }