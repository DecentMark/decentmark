from django.urls import path
from decentmark import views

app_name = 'decentmark'

urlpatterns = [
    path('', views.unit_list, name='unit_list'),
    path('u/create/', views.unit_create, name='unit_create'),
    # Unit required
    path('u/<int:unit_id>/', views.unit_view, name='unit_view'),
    path('u/<int:unit_id>/edit/', views.unit_edit, name='unit_edit'),
    path('u/<int:unit_id>/people/', views.people_list, name='people_list'),
    path('u/<int:unit_id>/invite/', views.unit_users_invite, name='unit_users_invite'),
    path('u/<int:unit_id>/log/', views.audit_log, name='audit_log'),
    path('u/<int:unit_id>/create_assignment/', views.assignment_create, name='assignment_create'),
    path('u/<int:unit_id>/assignments/', views.assignment_list, name='assignment_list'),
    # Assignment required
    path('a/<int:assignment_id>/', views.assignment_view, name='assignment_view'),
    path('a/<int:assignment_id>/edit/', views.assignment_edit, name='assignment_edit'),
    path('a/<int:assignment_id>/submissions/', views.submission_list, name='submission_list'),
    path('a/<int:assignment_id>/submit/', views.submission_create, name='submission_create'),
    # Submission required
    path('s/<int:submission_id>/', views.submission_view, name='submission_view'),
    path('s/<int:submission_id>/mark/', views.submission_mark, name='submission_mark'),
]
