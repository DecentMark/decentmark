from celery import Celery
from mako.template import Template


SOLUTION_VARIABLE = '${SOLUTION}'
TEST_CASE_VARIABLE = '${TEST_CASE}'
JOB_TEMPLATE = '''
import json
${IMPORTS}

${HELPER_CODE}

${HEADER}
    %s


if __name__ == '__main__':
    print(json.dumps(%s))
''' % (SOLUTION_VARIABLE, TEST_CASE_VARIABLE)

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

    job = Template(JOB_TEMPLATE).render(
        IMPORTS='',
        HELPER_CODE='',
        HEADER=submission.assignment.template,
        SOLUTION=SOLUTION_VARIABLE,
        TEST_CASE=TEST_CASE_VARIABLE
    )

    global_var = {
        'JOB': job,
        'STUDENT_SOLUTION': submission.solution,
        'TEACHER_SOLUTION': submission.assignment.solution
    }
    local_var = {}
    exec(submission.assignment.test, global_var, local_var)

    submission.autostatus = 'M'
    submission.automark = local_var['AUTOMARK']
    submission.autofeedback = local_var['AUTOFEEDBACK']
    submission.save()
