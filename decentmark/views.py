from datetime import datetime as Datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404

from decentmark.decorators import model_object_required, unit_permissions_required, modify_request
from decentmark.forms import UnitForm, AssignmentForm, SubmissionForm, FeedbackForm, \
    UserForm, UnitUsersForm
from decentmark.models import Unit, Assignment, Submission, AuditLog, UnitUsers


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
    # TODO: Use a permission for this
    if not request.user.is_staff:
        raise PermissionDenied("You need staff permission to create new units")

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
def user_invite(request) -> HttpResponse:
    """
    User Invite - Invite a new User
    """

    # TODO: Use a permission for this
    if not request.user.is_staff:
        raise PermissionDenied("You need staff permission to invite new members")

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError as error:
                pass
            return redirect('decentmark:unit_list')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = UserForm()

    return render(request, 'decentmark/user_invite.html', {'form': form})


@login_required
@model_object_required(Unit)
@unit_permissions_required(lambda uu: uu.create)
def unit_users_invite(request) -> HttpResponse:
    """
    UnitUsers Invite - Invite a new UnitUsers
    """

    if request.method == 'POST':
        form = UnitUsersForm(request.POST)
        if form.is_valid():
            new_unit_users = form.save(commit=False)
            new_unit_users.unit = request.unit
            form.save()
            return redirect(request.unit)
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
            feedback.marked = True
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
