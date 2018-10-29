from django.contrib.auth.models import User

from decentmark.models import Submission
from decentmark.celery import app


@app.task(
    bind=True,
    name='tasks.automatic_mark_and_feedback',
    ignore_result=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    acks_late=True,
)
def automatic_mark_and_feedback(self, submission_id):
    submission = Submission.objects.get(pk=submission_id)
    submission.autostatus = 'P'

    global_var = {
        'STUDENT_SOLUTION': submission.solution,
        'TEACHER_SOLUTION': submission.assignment.solution,
        'AUTOMARK': 0,
        'AUTOFEEDBACK': ''
    }
    try:
        exec(submission.assignment.test, global_var)
    except SystemExit:
        pass

    submission.autostatus = 'M'
    submission.automark = global_var['AUTOMARK']
    submission.autofeedback = global_var['AUTOFEEDBACK']
    submission.save()


@app.task(
    bind=True,
    name='tasks.email_user',
    ignore_result=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    acks_late=True,
)
def email_user(self, username, subject, message):
    user = User.objects.get(username=username)
    user.email_user(
        subject,
        message,
        fail_silently=False
    )
