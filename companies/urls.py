from django.urls import path

from .views import (
    company_create_view,
    company_detail_view,
    company_edit_view
)

urlpatterns = [
    path(
        'create/',
        company_create_view,
        name='company_create'
    ),

    path(
        'edit/',
        company_edit_view,
        name='company_edit'
    ),

    path(
        '',
        company_detail_view,
        name='company'
    ),
]