from rest_framework.views import APIView
from rest_framework.response import Response

from jobs.models import Job
from .serializers import JobSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from jobs.models import Job
from .serializers import JobSerializer, ApplicationSerializer

from rest_framework.permissions import IsAuthenticated
from companies.models import Company

from django.shortcuts import get_object_or_404
from applications.models import Application

class JobListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        jobs = Job.objects.filter(
            is_active=True
        )

        serializer = JobSerializer(
            jobs,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):
        if request.user.profile.user_type != 'recruiter':
            return Response(
                {
                    'error': 'Only recruiters can create jobs.'
                },
                status=status.HTTP_403_FORBIDDEN
    )

        company = Company.objects.filter(
            recruiter=request.user
        ).first()

        if company is None:
            return Response(
            {
                'error': 'You must create a company before posting a job.'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

        serializer = JobSerializer(
            data=request.data
                 )

        if serializer.is_valid():

            serializer.save(
            company=company
        )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
        )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
    )


class JobDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        job = get_object_or_404(
            Job,
            id=pk,
            is_active=True
        )

        serializer = JobSerializer(job)

        return Response(serializer.data)

    def put(self, request, pk):

        job = get_object_or_404(
            Job,
            id=pk,
            company__recruiter=request.user
        )

        serializer = JobSerializer(
            job,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(
                company=job.company
            )

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):

        job = get_object_or_404(
            Job,
            id=pk,
            company__recruiter=request.user
        )

        serializer = JobSerializer(
            job,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save(
                company=job.company
            )

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def delete(self, request, pk):

        job = get_object_or_404(
            Job,
            id=pk,
            company__recruiter=request.user
        )

        job.delete()

        return Response(
            {
                'message': 'Job deleted successfully.'
            },
            status=status.HTTP_204_NO_CONTENT
    )


class ApplyJobAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,job_id):
        if request.user.profile.user_type != 'job_seeker':
            return Response(
                {
                    'error':'Only job seekers can apply for jobs.'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        job = get_object_or_404(
            Job,
            id=job_id,
            is_active=True
        )

        if Application.objects.filter(
            job=job,
            applicant=request.user
        ).exists():
            return Response(
                {
                    'error':'You have already applied for this job.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer=ApplicationSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(
                job=job,
                applicant=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class MyApplicationsAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        applications=Application.objects.filter(
            applicant=request.user
        ).select_related(
            'job',
            'job__company'
        ).order_by('-applied_at')

        serializer=ApplicationSerializer(
            applications,
            many=True
        )

        return Response(
            serializer.data
        )

class RecruiterApplicantsAPIView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):

        if request.user.profile.user_type != 'recruiter':
            return Response(
                {
                    'error':'Only recruiters can view applicants,'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        applications=Application.objects.filter(
            job__company__recruiter=request.user
        ).select_related(
            'job',
            'applicant'
        ).order_by('-applied_at')

        serializer = ApplicationSerializer(
            applications,
            many=True
        )

        return Response(
            serializer.data
        )

class UpdateApplicationStatusAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, application_id):

        application = get_object_or_404(
            Application,
            id=application_id,
            job__company__recruiter=request.user
        )

        status_value = request.data.get('status')

        allowed_statuses = [
            'applied',
            'shortlisted',
            'rejected',
            'selected'
        ]

        if status_value not in allowed_statuses:
            return Response(
                {
                    'error': 'Invalid status.',
                    'allowed_statuses': allowed_statuses
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = status_value
        application.save()

        serializer = ApplicationSerializer(application)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )