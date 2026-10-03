from django.urls import path

from .views import (
    JobListAPIView,
    JobDetailAPIView,
    ApplyJobAPIView,
    MyApplicationsAPIView,
    RecruiterApplicantsAPIView,
    UpdateApplicationStatusAPIView
)


urlpatterns = [
    path(
        'jobs/',
        JobListAPIView.as_view(),
        name='api_job_list'
    ),
     path(
        'jobs/<int:pk>/',
        JobDetailAPIView.as_view(),
        name='api_job_detail'
    ),
    path(
    'jobs/<int:job_id>/apply/',
    ApplyJobAPIView.as_view(),
    name='api_apply_job'
    ),
    path(
    'my-applications/',
    MyApplicationsAPIView.as_view(),
    name='api_my_applications'

     ),

     path(
    'recruiter/applicants/',
    RecruiterApplicantsAPIView.as_view(),
    name='api_recruiter_applicants'
    ),
     path(
    'applications/<int:application_id>/status/',
    UpdateApplicationStatusAPIView.as_view(),
    name='api_update_application_status'
    ),
]
