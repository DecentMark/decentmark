'''
Example marking script for the following assignment set up

Solution
def sum(a, b):
    return a + b

Template
def sum(a, b):
'''

from marker.jobrunner import get_result
import sys
import json

AUTOMARK = 0
AUTOFEEDBACK = ''
LANGUAGE = 'python3'

if 'import' in STUDENT_SOLUTION:
    AUTOFEEDBACK = 'The word "import" was found in your code.'
    sys.exit(0)

test_cases = ['sum(1, 2)', 'sum(2, 5)']

for t in test_cases:
    student_result = get_result(LANGUAGE, STUDENT_SOLUTION, t)
    teacher_result = get_result(LANGUAGE, TEACHER_SOLUTION, t)

    # check if result objects are empty
    if not student_result or not teacher_result:
        AUTOFEEDBACK += '204 occurred\n'
        continue

    student_stdout = student_result['stdout']
    teacher_stdout = teacher_result['stdout']

    # load standard output if not an empty string
    if student_stdout:
        student_stdout = json.loads(student_stdout)
    if teacher_stdout:
        teacher_stdout = json.loads(teacher_stdout)

    if student_stdout == teacher_stdout:
        AUTOMARK += 1
        AUTOFEEDBACK += 'correct\n'
    else:
        AUTOFEEDBACK += 'incorrect\n'
