import random
import string

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from marker import tasks
from decentmark.decorators import model_object_required, unit_permissions_required, modify_request
from decentmark.forms import UnitForm, AssignmentForm, SubmissionForm, FeedbackForm, \
    UnitUsersForm
from decentmark.models import Unit, Assignment, Submission, AuditLog, UnitUsers

def about(request) -> HttpResponse:
    """
    About - About Decentmark
    """

    context = {
    }

    return render(request, 'decentmark/about.html', context)

@login_required
@model_object_required(Unit)
@unit_permissions_required(lambda uu: uu.create)
def audit_log(request) -> HttpResponse:
    """
    Audit Log - Events recorded in the unit.
    People with create permission can view this.
    """

    log = AuditLog.objects.filter(unit=request.unit).order_by('-date', '-id')

    log_count = log.count()

    context = {
        "unit": request.unit,
        "audit_log": log,
        "audit_log_count": log_count,
    }

    return render(request, 'decentmark/audit_log.html', context)

@login_required
def unit_list(request) -> HttpResponse:
    """
    Unit List - List of units. Staff see all units. Non-staff see units they are enrolled in.
    """

    # Get units they have access to
    accessible_unit_ids = UnitUsers.objects.filter(user=request.user).values_list('unit__id', flat=True)
    # Filter by those units
    unit_list = Unit.objects.filter(id__in=accessible_unit_ids)

    unit_count = unit_list.count()

    context = {
        "unit_list": unit_list,
        "unit_count": unit_count,
    }

    return render(request, 'decentmark/unit_list.html', context)


@login_required
def unit_create(request) -> HttpResponse:
    """
    Unit Create - Create a new Unit
    """
    # # TODO: Use a permission for this
    # if not request.user.is_staff:
    #     raise PermissionDenied("You need staff permission to create new units")

    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save()
            # Give all permissions to the creator of the unit
            UnitUsers.objects.create(user=request.user, unit=unit, create=True, mark=True, submit=True)
            return redirect(unit)
        else:
            for error in form.non_field_errors():
                messages.error(request, error)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UnitForm()

    return render(request, 'decentmark/unit_create.html', {'form': form})


@login_required
@model_object_required(Unit)
@unit_permissions_required(lambda uu: uu.create)
def unit_edit(request) -> HttpResponse:
    """
    Unit Edit - Edit a Unit
    Requires Create permission on the unit
    """

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=request.unit)
        if form.is_valid():
            unit = form.save()
            return redirect(unit)
        else:
            for error in form.non_field_errors():
                messages.error(request, error)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UnitForm(instance=request.unit)

    context = {
        'form': form,
        'unit': request.unit,
    }

    return render(request, 'decentmark/unit_edit.html', context)


@login_required()
@model_object_required(Unit)
@unit_permissions_required(lambda uu: True)
def unit_view(request) -> HttpResponse:
    """
    Unit View - View unit details
    """

    context = {
        "unit": request.unit,
    }

    return render(request, 'decentmark/unit_view.html', context)


@login_required
@model_object_required(Unit)
@unit_permissions_required(lambda uu: True)
def people_list(request) -> HttpResponse:
    """
    People List - List of UnitUsers.
    """

    people_list = UnitUsers.objects.filter(unit=request.unit)

    people_count = people_list.count()

    context = {
        "unit": request.unit,
        "people_list": people_list,
        "people_count": people_count,
    }

    return render(request, 'decentmark/people_list.html', context)


def get_users_info(file):
    users = []
    for line in file:
        try:
            email, tag, first_name, last_name = line.decode('utf-8').strip().split(',')
        except ValueError:
            continue
        try:
            validate_email(email)
        except ValidationError:
            continue
        users.append({
            'email': email,
            'tag': tag,
            'first name': first_name,
            'last name': last_name
        })
    return users


def get_user(email, first_name, last_name):
    # make username the email for now
    username = email
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
        user = User.objects.create_user(
            username,
            email,
            password,
            first_name=first_name,
            last_name=last_name
        )
        user.email_user(
            'account creation',
            'username: %s\npassword: %s' % (user.get_username(), password),
            fail_silently=False
        )
    return user


def create_unit_user(user, unit, create, mark, submit, tag):
    unit_users = UnitUsers(
        user=user,
        unit=unit,
        create=create,
        mark=mark,
        submit=submit,
        tag=tag
    )
    unit_users.save()
    user.email_user(
        'unit invitation',
        'welcome to %s' % unit,
        fail_silently=False
    )


@login_required
@model_object_required(Unit)
@unit_permissions_required(lambda uu: uu.create)
def unit_users_invite(request) -> HttpResponse:
    """
    UnitUsers Invite - Invite new UnitUsers
    """

    if request.method == 'POST':
        form = UnitUsersForm(request.POST, request.FILES)
        if form.is_valid():
            users = get_users_info(request.FILES['users'])
            for u in users:
                user = get_user(u['email'], u['first name'], u['last name'])
                if not UnitUsers.objects.all().filter(user=user, unit=request.unit).exists():
                    create_unit_user(
                        user,
                        request.unit,
                        form.cleaned_data['create'],
                        form.cleaned_data['mark'],
                        form.cleaned_data['submit'],
                        u['tag']
                    )
            return redirect(reverse('decentmark:people_list', args=(request.unit.id,)))
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = UnitUsersForm()

    context = {
        'form': form,
        'unit': request.unit,
    }

    return render(request, 'decentmark/unit_users_invite.html', context)


@login_required
@model_object_required(Unit)
@unit_permissions_required(lambda uu: uu.create)
def assignment_create(request) -> HttpResponse:
    """
    Assignment Create - Create a new Assignment
    """

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.unit = request.unit
            assignment = form.save()
            # TODO: Consider having the creator make a submission using the solution
            return redirect(assignment)
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = AssignmentForm()

    context = {
        'form': form,
        'unit': request.unit,
    }

    return render(request, 'decentmark/assignment_create.html', context)


@login_required
@model_object_required(Assignment)
@modify_request('unit', lambda r: r.assignment.unit)
@unit_permissions_required(lambda uu: uu.create)
def assignment_edit(request) -> HttpResponse:
    """
    Assignment Edit - Edit an existing Assignment
    """

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=request.assignment)
        if form.is_valid():
            assignment = form.save()
            AuditLog.objects.create(unit=request.unit, message="%s[%s] edited %s[%s]" % (request.user, request.user.pk, request.assignment, request.assignment.pk))
            # TODO: Consider having the creator make a submission using the solution
            return redirect(assignment)
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = AssignmentForm(instance=request.assignment)

    context = {
        'form': form,
        'unit': request.unit,
        'assignment': request.assignment,
    }

    return render(request, 'decentmark/assignment_edit.html', context)


@login_required
@model_object_required(Unit)
@unit_permissions_required(lambda uu: True)
def assignment_list(request) -> HttpResponse:
    """
    Assignment List - List of assignments.
    All assignments are visible for now.
    (Later?) Staff see all assignments. Non-staff see open assignments.
    """

    # Staff
    # if request.unit_user.create or request.unit_user.mark:
    assignment_list = Assignment.objects.filter(unit=request.unit).order_by('start')
    # else:
    #     # TODO: Filter by start > today
    #     today = Datetime.today()
    #     assignment_list = Assignment.objects.filter(unit=request.unit).filter(start__gte=today).order_by('start')

    assignment_count = assignment_list.count()

    context = {
        "unit": request.unit,
        "assignment_list": assignment_list,
        "assignment_count": assignment_count,
    }

    return render(request, 'decentmark/assignment_list.html', context)


@login_required()
@model_object_required(Assignment)
@modify_request('unit', lambda r: r.assignment.unit)
@unit_permissions_required(lambda uu: True)
def assignment_view(request) -> HttpResponse:
    """
    Assignment View - View assignment details
    Anyone part of the unit can view an assignment
    """
    # TODO: Restrictions?

    context = {
        "unit": request.unit,
        "assignment": request.assignment,
    }

    return render(request, 'decentmark/assignment_view.html', context)


@login_required
@model_object_required(Assignment)
@modify_request('unit', lambda r: r.assignment.unit)
@unit_permissions_required(lambda uu: True)
def submission_list(request) -> HttpResponse:
    """
    Submission List - List of submissions.
    Markers see all submissions. Otherwise only own submissions.
    """

    if request.unit_user.mark:
        submission_list = Submission.objects.filter(assignment=request.assignment).order_by('date')
    else:
        submission_list = Submission.objects.filter(assignment=request.assignment).filter(user=request.user).order_by('date')

    context = {
        "unit": request.unit,
        "assignment": request.assignment,
        "submission_list": submission_list,
    }

    return render(request, 'decentmark/submission_list.html', context)


@login_required
@model_object_required(Assignment)
@modify_request('unit', lambda r: r.assignment.unit)
@unit_permissions_required(lambda uu: uu.submit)
def submission_create(request) -> HttpResponse:
    """
    Submission Create - Make a submission
    """
    if request.method == 'POST':
        form = SubmissionForm(request.POST, initial={
            'assignment': request.assignment,
        })
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.assignment = request.assignment
            submission = form.save()
            tasks.automatic_mark_and_feedback(submission)
            AuditLog.objects.create(unit=request.unit, message="%s[%s] submitted %s[%s]" % (request.user, request.user.pk, submission, submission.pk))
            return redirect(submission)
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = SubmissionForm()

    context = {
        'form': form,
        'unit': request.unit,
        'assignment': request.assignment,
    }

    return render(request, 'decentmark/submission_create.html', context)


@login_required()
@model_object_required(Submission)
@modify_request('assignment', lambda r: r.submission.assignment)
@modify_request('unit', lambda r: r.assignment.unit)
@unit_permissions_required(lambda uu: True)
def submission_view(request) -> HttpResponse:
    """
    Submission View - View submission details
    Can view a submission if a marker, or owner of the submission
    """

    if not request.unit_user.mark and request.user != request.submission.user:
        raise PermissionDenied

    context = {
        "unit": request.unit,
        "assignment": request.assignment,
        "submission": request.submission,
    }

    return render(request, 'decentmark/submission_view.html', context)


@login_required
@model_object_required(Submission)
@modify_request('assignment', lambda r: r.submission.assignment)
@modify_request('unit', lambda r: r.assignment.unit)
@unit_permissions_required(lambda uu: uu.mark)
def submission_mark(request) -> HttpResponse:
    """
    Submission Mark - Mark a submission
    """

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=request.submission)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback = form.save()
            AuditLog.objects.create(unit=request.unit, message="%s[%s] marked %s[%s]" % (request.user, request.user.pk, request.submission, request.submission.pk))
            return redirect(feedback)
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = FeedbackForm(instance=request.submission)

    context = {
        'form': form,
        'unit': request.unit,
        'assignment': request.assignment,
        'submission': request.submission,
    }

    return render(request, 'decentmark/submission_mark.html', context)
