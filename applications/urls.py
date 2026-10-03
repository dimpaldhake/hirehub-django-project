from django.urls import path

from .views import (
    apply_job_view,
    my_applications_view,
    recruiter_applicants_view,
    recruiter_job_applicants_view,
    update_application_status_view,
    recruiter_application_detail_view
)


urlpatterns = [

    path(
        'jobs/<int:job_id>/apply/',
        apply_job_view,
        name='apply_job'
    ),

    path(
        'my-applications/',
        my_applications_view,
        name='my_applications'
    ),

    path(
        'recruiter/applicants/',
        recruiter_applicants_view,
        name='recruiter_applicants'
    ),

    path(
        'recruiter/applicants/job/<int:job_id>/',
        recruiter_job_applicants_view,
        name='recruiter_job_applicants'
    ),

    path(
        'recruiter/applicants/<int:application_id>/status/',
        update_application_status_view,
        name='update_application_status'
    ),

    path(
    'recruiter/applicants/application/<int:application_id>/',
    recruiter_application_detail_view,
    name='recruiter_application_detail'
    ),
]