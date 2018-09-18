from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404

from decentmark.decorators import model_object_required
from decentmark.forms import UnitForm, AssignmentForm, SubmissionForm, FeedbackForm, \
    UserForm, UnitUsersForm
from decentmark.models import Unit, Assignment, Submission, AuditLog


@login_required
@model_object_required(Unit)
def audit_log(request, unit=None) -> HttpResponse:
    """
    Assignment List - List of assignments.
    Staff see all assignments. Non-staff see open assignments.
    """

    # TODO: Limit this to only teacher
    log = AuditLog.objects.filter(unit=unit).order_by('date', 'id')

    log_count = log.count()

    context = {
        "unit": unit,
        "audit_log": log,
        "audit_log_count": log_count,
    }

    return render(request, 'decentmark/audit_log.html', context)

@login_required
def unit_list(request) -> HttpResponse:
    """
    Unit List - List of units. Staff see all units. Non-staff see units they are enrolled in.
    """

    # Staff
    if request.user.is_staff:
        unit_list = Unit.objects.all().order_by('name')
    else:
        # TODO: Filter by unit users
        unit_list = Unit.objects.all().order_by('name')
        # unit_list = Unit.objects.filter(user=request.user).order_by('name')

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
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('decentmark:unit_list')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UnitForm()

    return render(request, 'decentmark/unit_create.html', {'form': form})


@login_required
@model_object_required(Unit)
def unit_edit(request, unit=None) -> HttpResponse:
    """
    Unit Create - Create a new Unit
    """

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('decentmark:unit_list')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UnitForm(instance=unit)

    context = {
        'form': form,
        'unit': unit,
    }

    return render(request, 'decentmark/unit_edit.html', context)


@login_required()
@model_object_required(Unit)
def unit_view(request, unit=None) -> HttpResponse:
    """
    Unit View - View unit details
    """

    context = {
        "unit": unit,
    }

    return render(request, 'decentmark/unit_view.html', context)


@login_required
def user_invite(request) -> HttpResponse:
    """
    User Invite - Invite a new User
    """
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
def unit_users_invite(request, unit=None) -> HttpResponse:
    """
    UnitUsers Invite - Invite a new UnitUsers
    """

    if request.method == 'POST':
        form = UnitUsersForm(request.POST)
        if form.is_valid():
            new_unit_users = form.save(commit=False)
            new_unit_users.unit = unit
            form.save()
            return redirect('decentmark:unit_list')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = UnitUsersForm()

    context = {
        'form': form,
        'unit': unit,
    }

    return render(request, 'decentmark/unit_users_invite.html', context)


@login_required
@model_object_required(Unit)
def assignment_create(request, unit=None) -> HttpResponse:
    """
    Assignment Create - Create a new Assignment
    """

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            new_assignment = form.save(commit=False)
            new_assignment.unit = unit
            form.save()
            return redirect(reverse('decentmark:assignment_list', args=(unit.id,)))
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = AssignmentForm()

    context = {
        'form': form,
        'unit': unit,
    }

    return render(request, 'decentmark/assignment_create.html', context)


@login_required
@model_object_required(Assignment)
def assignment_edit(request, assignment=None) -> HttpResponse:
    """
    Assignment Edit - Edit an existing Assignment
    """
    unit = assignment.unit

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect(reverse('decentmark:assignment_list', args=(unit.id,)))
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = AssignmentForm(instance=assignment)

    context = {
        'form': form,
        'unit': unit,
        'assignment': assignment,
    }

    return render(request, 'decentmark/assignment_edit.html', context)


@login_required
def assignment_list(request, unit_id=None) -> HttpResponse:
    """
    Assignment List - List of assignments.
    Staff see all assignments. Non-staff see open assignments.
    """

    unit = get_object_or_404(Unit, id=unit_id)

    # Staff
    if request.user.is_staff:
        assignment_list = Assignment.objects.filter(unit=unit).order_by('start')
    else:
        # TODO: Filter by start > today
        assignment_list = Assignment.objects.filter(unit=unit).order_by('start')

    assignment_count = assignment_list.count()

    context = {
        "unit": unit,
        "assignment_list": assignment_list,
        "assignment_count": assignment_count,
    }

    return render(request, 'decentmark/assignment_list.html', context)


@login_required()
@model_object_required(Assignment)
def assignment_view(request, assignment=None) -> HttpResponse:
    """
    Assignment View - View assignment details
    """
    unit = assignment.unit

    context = {
        "unit": unit,
        "assignment": assignment,
    }

    return render(request, 'decentmark/assignment_view.html', context)


@login_required
@model_object_required(Assignment)
def submission_list(request, assignment=None) -> HttpResponse:
    """
    Submission List - List of submissions.
    Staff see all submissions. Non-staff see their own submissions.
    """
    unit = assignment.unitg

    # Staff
    if request.user.is_staff:
        submission_list = Submission.objects.filter(assignment=assignment).order_by('date')
    else:
        # TODO: Filter by user = request.user
        submission_list = Submission.objects.filter(assignment=assignment).order_by('date')

    context = {
        "unit": unit,
        "assignment": assignment,
        "submission_list": submission_list,
    }

    return render(request, 'decentmark/submission_list.html', context)


@login_required
@model_object_required(Assignment)
def submission_create(request, assignment=None) -> HttpResponse:
    """
    Submission Create - Make a submission
    """
    unit = assignment.unit

    if request.method == 'POST':
        form = SubmissionForm(request.POST, initial={
            'assignment': assignment,
        })
        if form.is_valid():
            new_submission = form.save(commit=False)
            new_submission.user = request.user
            new_submission.assignment = assignment
            form.save()
            return redirect(reverse('decentmark:assignment_view', args=(assignment.id,)))
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = SubmissionForm()

    context = {
        'form': form,
        'unit': unit,
        'assignment': assignment,
    }

    return render(request, 'decentmark/submission_create.html', context)


@login_required()
@model_object_required(Submission)
def submission_view(request, submission=None) -> HttpResponse:
    """
    Submission View - View submission details
    """
    assignment = submission.assignment
    unit = assignment.unit

    context = {
        "unit": unit,
        "assignment": assignment,
        "submission": submission,
    }

    return render(request, 'decentmark/submission_view.html', context)


@login_required
@model_object_required(Submission)
def submission_mark(request, submission=None) -> HttpResponse:
    """
    Submission Mark - Mark a submission
    """
    assignment = submission.assignment
    unit = assignment.unit

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=submission)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.marked = True
            form.save()
            return redirect(reverse('decentmark:submission_view', args=(submission.id,)))
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = FeedbackForm(instance=submission)

    context = {
        'form': form,
        'unit': unit,
        'assignment': assignment,
        'submission': submission,
    }

    return render(request, 'decentmark/submission_mark.html', context)
