from celery import Celery

app = Celery('tasks')


@app.task
def automatic_feedback(submission):
    submission.marked = True
    submission.mark = 1
    submission.feedback = 'here is your automatic feedback'
    submission.save()
