from rest_framework import serializers
from applications.models import Application

from jobs.models import Job


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job

        fields = (
            'id',
            'company',
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
            'created_at',
            'updated_at',
        )

        read_only_fields = (
            'id',
            'company',
            'created_at',
            'updated_at',
        )


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application

        fields = (
            'id',
            'job',
            'applicant',
            'resume',
            'cover_letter',
            'status',
            'applied_at',
            'updated_at',
        )

        read_only_fields = (
            'id',
            'job',
            'applicant',
            'status',
            'applied_at',
            'updated_at',
        )