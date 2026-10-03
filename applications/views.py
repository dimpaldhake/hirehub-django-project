from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Application
from .forms import ApplicationForm
from jobs.models import Job


# =========================================================
# APPLY FOR JOB
# =========================================================

@login_required
def apply_job_view(request, job_id):

    job = get_object_or_404(Job, id=job_id)

    # Only Job Seekers can apply
    if request.user.profile.user_type != 'job_seeker':
        return redirect('job_detail', pk=job.id)

    # Job must be active
    if not job.is_active:
        return render(
            request,
            'applications/job_not_available.html',
            {
                'job': job,
                'reason': 'inactive'
            }
        )

    # Deadline check
    from django.utils import timezone

    if job.deadline < timezone.localdate():
        return render(
            request,
            'applications/job_not_available.html',
            {
                'job': job,
                'reason': 'expired'
            }
        )

    # Prevent duplicate application
    if Application.objects.filter(
        job=job,
        applicant=request.user
    ).exists():

        return render(
            request,
            'applications/already_applied.html',
            {
                'job': job
            }
        )

    # Submit application
    if request.method == 'POST':

        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(commit=False)

            application.job = job
            application.applicant = request.user

            application.save()

            return redirect('my_applications')

    else:

        form = ApplicationForm()

    return render(
        request,
        'applications/apply_job.html',
        {
            'form': form,
            'job': job
        }
    )


# =========================================================
# JOB SEEKER - MY APPLICATIONS
# =========================================================

@login_required
def my_applications_view(request):

    applications = (
        Application.objects
        .filter(applicant=request.user)
        .select_related(
            'job',
            'job__company'
        )
        .order_by('-applied_at')
    )

    return render(
        request,
        'applications/my_applications.html',
        {
            'applications': applications
        }
    )


# =========================================================
# RECRUITER - ALL APPLICANTS
# =========================================================

@login_required
def recruiter_applicants_view(request):

    # Only recruiters can access this page
    if request.user.profile.user_type != 'recruiter':
        return redirect('job_list')

    applications = (
        Application.objects
        .filter(
            job__company__recruiter=request.user
        )
        .select_related(
            'job',
            'applicant'
        )
        .order_by('-applied_at')
    )

    return render(
        request,
        'applications/recruiter_applicants.html',
        {
            'applications': applications
        }
    )


# =========================================================
# RECRUITER - APPLICANTS FOR ONE JOB
# =========================================================

@login_required
def recruiter_job_applicants_view(request, job_id):

    # Only recruiters can access this page
    if request.user.profile.user_type != 'recruiter':
        return redirect('job_list')

    # Recruiter can only access their own job
    job = get_object_or_404(
        Job,
        id=job_id,
        company__recruiter=request.user
    )

    applications = (
        Application.objects
        .filter(job=job)
        .select_related(
            'applicant'
        )
        .order_by('-applied_at')
    )

    return render(
        request,
        'applications/recruiter_job_applicants.html',
        {
            'job': job,
            'applications': applications
        }
    )


# =========================================================
# RECRUITER - CANDIDATE DETAIL
# =========================================================

@login_required
def recruiter_application_detail_view(
    request,
    application_id
):

    # Only recruiters can access candidate details
    if request.user.profile.user_type != 'recruiter':
        return redirect('job_list')

    # Recruiter can only see candidates
    # who applied to their own jobs
    application = get_object_or_404(

        Application.objects.select_related(
            'applicant',
            'applicant__profile',
            'job',
            'job__company'
        ),

        id=application_id,

        job__company__recruiter=request.user
    )

    return render(
        request,
        'applications/recruiter_application_detail.html',
        {
            'application': application
        }
    )


# =========================================================
# RECRUITER - UPDATE APPLICATION STATUS
# =========================================================

@login_required
def update_application_status_view(
    request,
    application_id
):

    # Get only applications belonging
    # to recruiter's own jobs
    application = get_object_or_404(
        Application,
        id=application_id,
        job__company__recruiter=request.user
    )

    if request.method == 'POST':

        status = request.POST.get('status')

        # Allowed application statuses
        allowed_statuses = [
            'applied',
            'shortlisted',
            'rejected',
            'selected'
        ]

        if status in allowed_statuses:

            application.status = status

            application.save()

    # After updating, return to applicants
    # page for the same job
    return redirect(
        'recruiter_job_applicants',
        job_id=application.job.id
    )