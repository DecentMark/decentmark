from celery import Celery


app = Celery('tasks')


@app.task(
    name='tasks.automatic_mark_and_feedback',
    ignore_result=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    acks_late=True,
    max_retries=10
)
def automatic_mark_and_feedback(submission):

    submission.autostatus = 'P'

    global_var = {
        'STUDENT_SOLUTION': submission.solution,
        'TEACHER_SOLUTION': submission.assignment.solution
    }

    try:
        exec(submission.assignment.test, global_var)
    except SystemExit:
        pass

    submission.autostatus = 'M'
    submission.automark = global_var['AUTOMARK']
    submission.autofeedback = global_var['AUTOFEEDBACK']
    submission.save()
