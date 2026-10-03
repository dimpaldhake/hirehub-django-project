from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from applications.models import Application
from jobs.models import Job


@login_required
def dashboard_view(request):

    # =====================================================
    # JOB SEEKER DASHBOARD
    # =====================================================

    if request.user.profile.user_type == 'job_seeker':

        applications = (
            Application.objects
            .filter(applicant=request.user)
            .select_related(
                'job',
                'job__company'
            )
            .order_by('-applied_at')
        )

        context = {

            'total_applications': applications.count(),

            'applied_count': applications.filter(
                status='applied'
            ).count(),

            'shortlisted_count': applications.filter(
                status='shortlisted'
            ).count(),

            'selected_count': applications.filter(
                status='selected'
            ).count(),

            'rejected_count': applications.filter(
                status='rejected'
            ).count(),

            # Latest applications
            'recent_applications': applications[:5],
        }

        return render(
            request,
            'dashboard/job_seeker_dashboard.html',
            context
        )


    # =====================================================
    # RECRUITER DASHBOARD
    # =====================================================

    elif request.user.profile.user_type == 'recruiter':

        jobs = (
            Job.objects
            .filter(
                company__recruiter=request.user
            )
            .select_related(
                'company',
                'category'
            )
            .order_by('-created_at')
        )

        applications = (
            Application.objects
            .filter(
                job__company__recruiter=request.user
            )
            .select_related(
                'applicant',
                'applicant__profile',
                'job'
            )
            .order_by('-applied_at')
        )

        context = {

            # Job statistics
            'total_jobs': jobs.count(),

            'active_jobs': jobs.filter(
                is_active=True
            ).count(),

            # Applicant statistics
            'total_applicants': applications.count(),

            'shortlisted_count': applications.filter(
                status='shortlisted'
            ).count(),

            'selected_count': applications.filter(
                status='selected'
            ).count(),

            'rejected_count': applications.filter(
                status='rejected'
            ).count(),

            # Recent data
            'recent_jobs': jobs[:5],

            'recent_applicants': applications[:5],
        }

        return render(
            request,
            'dashboard/recruiter_dashboard.html',
            context
        )