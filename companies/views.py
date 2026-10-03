from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from .forms import CompanyForm
from .models import Company

@login_required
def company_create_view(request):

    if Company.objects.filter(recruiter=request.user).exists():
        return redirect('company')

    if request.method == 'POST':

        form = CompanyForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            company = form.save(commit=False)

            company.recruiter = request.user

            company.save()

            return redirect('company')

    else:

        form = CompanyForm()

    return render(
        request,
        'companies/company_create.html',
        {'form': form}
    )


@login_required
@login_required
def company_detail_view(request):

    company = Company.objects.filter(
        recruiter=request.user
    ).first()

    if company is None:
        return redirect('company_create')

    return render(
        request,
        'companies/company_detail.html',
        {'company': company}
    )

@login_required
def company_edit_view(request):

    company = Company.objects.get(
        recruiter = request.user
    )

    if request.method == 'POST':
        form = CompanyForm(
            request.POST,
            request.FILES,
            instance=company
        )

        if form.is_valid():
            form.save()
            return redirect('company')
    else:
        form =CompanyForm(
            instance=company
        )

    return render(
        request,
        'companies/company_edit.html',
        {'form':form}
    )