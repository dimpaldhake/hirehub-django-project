from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, ProfileForm
from .models import Profile
from jobs.models import Job

from django.contrib.auth.models import User
from companies.models import Company
from django.utils.http import url_has_allowed_host_and_scheme

def register_view(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            print("FORM IS VALID")

            user = form.save()

            print("USER CREATED:", user.username)

            Profile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type']
            )

            print("PROFILE CREATED")

            return redirect('login')

        else:

            print("FORM IS INVALID")
            print(form.errors)

    else:

        form = RegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

def login_view(request):

    next_url = request.GET.get('next') or request.POST.get('next') or ''

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # Send user to the page they originally wanted
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            # Otherwise go to Home
            return redirect('home')

        return render(
            request,
            'accounts/login.html',
            {
                'error': 'Invalid username or password.',
                'next': next_url
            }
        )

    return render(
        request,
        'accounts/login.html',
        {
            'next': next_url
        }
    )


def logout_view(request):

    logout(request)

    return redirect('login')




def home_view(request):

    latest_jobs = Job.objects.filter(
        is_active=True
    ).select_related(
        'company',
        'category'
    ).order_by(
        '-created_at'
    )[:6]

    active_jobs_count = Job.objects.filter(
        is_active=True
    ).count()

    users_count = User.objects.count()

    companies_count = Company.objects.count()

    return render(
        request,
        'home.html',
        {
            'latest_jobs': latest_jobs,
            'active_jobs_count': active_jobs_count,
            'users_count': users_count,
            'companies_count': companies_count,
        }
    )

@login_required
@login_required
def profile_view(request):

    profile = Profile.objects.get(user=request.user)

    skills = profile.skills.split(',') if profile.skills else []

    return render(
        request,
        'accounts/profile.html',
        {
            'profile': profile,
            'skills': skills,
        }
    )


@login_required
def profile_edit_view(request):

    profile = Profile.objects.get(
        user=request.user
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect('profile')

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'accounts/profile_edit.html',
        {
            'form': form
        }
    )