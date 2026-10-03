from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Job, Category
from .forms import JobForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from companies.models import Company

from django.db.models import Q, Count


# =========================================================
# JOB LIST
# =========================================================

class JobListView(ListView):

    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):

        query = self.request.GET.get('q')
        location = self.request.GET.get('location')
        job_type = self.request.GET.get('job_type')
        experience = self.request.GET.get('experience')
        category = self.request.GET.get('category')
        min_salary = self.request.GET.get('min_salary')
        max_salary = self.request.GET.get('max_salary')
        sort = self.request.GET.get('sort')

        jobs = Job.objects.filter(
            is_active=True
        )

        # Search
        if query:

            jobs = jobs.filter(
                Q(title__icontains=query) |
                Q(skills__icontains=query) |
                Q(description__icontains=query)
            )

        # Location
        if location:

            jobs = jobs.filter(
                location__icontains=location
            )

        # Job Type
        if job_type:

            jobs = jobs.filter(
                job_type=job_type
            )

        # Experience
        if experience:

            jobs = jobs.filter(
                experience__lte=experience
            )

        # Category
        if category:

            jobs = jobs.filter(
                category_id=category
            )

        # Minimum Salary
        if min_salary:

            jobs = jobs.filter(
                salary_max__gte=min_salary
            )

        # Maximum Salary
        if max_salary:

            jobs = jobs.filter(
                salary_min__lte=max_salary
            )

        # Sorting
        if sort == 'newest':

            jobs = jobs.order_by(
                '-created_at'
            )

        elif sort == 'oldest':

            jobs = jobs.order_by(
                'created_at'
            )

        elif sort == 'salary_low':

            jobs = jobs.order_by(
                'salary_min'
            )

        elif sort == 'salary_high':

            jobs = jobs.order_by(
                '-salary_min'
            )

        else:

            # Default sorting
            jobs = jobs.order_by(
                '-created_at'
            )

        return jobs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()

        return context


# =========================================================
# JOB DETAIL
# =========================================================

class JobDetailView(DetailView):

    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Convert skills text into a list
        context['skills'] = self.object.skills.split()

        # Check whether current user already applied
        context['already_applied'] = False

        if self.request.user.is_authenticated:

            context['already_applied'] = self.object.applications.filter(
                applicant=self.request.user
            ).exists()

        return context


# =========================================================
# CREATE JOB
# =========================================================

class JobCreateView(LoginRequiredMixin, CreateView):

    model = Job

    form_class = JobForm

    template_name = 'jobs/job_create.html'

    def dispatch(self, request, *args, **kwargs):

        # Only recruiters can create jobs
        if request.user.profile.user_type != 'recruiter':

            return redirect('job_list')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def form_valid(self, form):

        # Find the company owned by this recruiter
        company = Company.objects.filter(
            recruiter=self.request.user
        ).first()

        # Recruiter must create company first
        if company is None:

            return redirect('company_create')

        # Connect the job with the recruiter company
        form.instance.company = company

        return super().form_valid(form)

    def get_success_url(self):

        return f'/jobs/{self.object.pk}/'


# =========================================================
# UPDATE JOB
# =========================================================

class JobUpdateView(LoginRequiredMixin, UpdateView):

    model = Job

    form_class = JobForm

    template_name = 'jobs/job_edit.html'

    context_object_name = 'job'

    def dispatch(self, request, *args, **kwargs):

        # Only recruiters can update jobs
        if request.user.profile.user_type != 'recruiter':

            return redirect('job_list')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def get_queryset(self):

        # Recruiter can update only their own jobs
        return Job.objects.filter(
            company__recruiter=self.request.user
        )

    def get_success_url(self):

        return f'/jobs/{self.object.pk}/'


# =========================================================
# MY JOBS
# =========================================================

class MyJobsView(LoginRequiredMixin, ListView):

    model = Job

    template_name = 'jobs/my_jobs.html'

    context_object_name = 'jobs'

    def dispatch(self, request, *args, **kwargs):

        # Only recruiters can access My Jobs
        if request.user.profile.user_type != 'recruiter':

            return redirect('job_list')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def get_queryset(self):

        return (
            Job.objects
            .filter(
                company__recruiter=self.request.user
            )
            .select_related(
                'company',
                'category'
            )
            .annotate(

                # Total applicants
                applicant_count=Count(
                    'applications'
                ),

                # Shortlisted applicants
                shortlisted_count=Count(
                    'applications',
                    filter=Q(
                        applications__status='shortlisted'
                    )
                ),

                # Selected applicants
                selected_count=Count(
                    'applications',
                    filter=Q(
                        applications__status='selected'
                    )
                )

            )
            .order_by('-created_at')
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        jobs = self.get_queryset()

        context['total_jobs'] = jobs.count()

        context['active_jobs'] = jobs.filter(
            is_active=True
        ).count()

        return context


# =========================================================
# DELETE JOB
# =========================================================

class JobDeleteView(LoginRequiredMixin, DeleteView):

    model = Job

    template_name = 'jobs/job_confirm_delete.html'

    context_object_name = 'job'

    def dispatch(self, request, *args, **kwargs):

        # Only recruiters can delete jobs
        if request.user.profile.user_type != 'recruiter':

            return redirect('job_list')

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    def get_queryset(self):

        # Recruiter can delete only their own jobs
        return Job.objects.filter(
            company__recruiter=self.request.user
        )

    def get_success_url(self):

        return '/jobs/my-jobs/'