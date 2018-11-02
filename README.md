# DecentMark
Automatic grader for programming assignments.

## Running
- pip install -r requirements.txt
- python manage.py migrate
- cp decentsite/local_settings_example.py decentsite/local_settings.py
- python manage.py runserver --settings decentsite.local_settings

## Marking
- Install and setup RabbitMQ
- sudo rabbitmq-server
- celery -A decentmark worker -l info

## Testing
- Download Selenium driver for your OS and add it to the path environment variable.
- python manage.py test

## References
- [django](https://www.djangoproject.com/) the web framework and its examples
- [gitignore.io](https://www.gitignore.io/)
- [django-todo](https://github.com/shacker/django-todo) for its examples
- [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks) for adding css to forms
