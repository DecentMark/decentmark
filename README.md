# DecentMark
Automatic grader for programming assignments.

## Running
- pip install -r requirements.txt
- python manage.py migrate --settings decentsite.local_settings
- cp decentsite/local_settings_example.py decentsite/local_settings.py
- python manage.py runserver --settings decentsite.local_settings

## Marking
- Install and setup RabbitMQ
- sudo rabbitmq-server
- celery -A decentmark worker -l info
- For windows: `celery -A decentmark worker --pool=eventlet -l info`

## Testing
- Download Selenium driver for your OS and add it to the path environment variable.
- python manage.py test

## RabbitMQ for development
- `docker run -d --hostname rabbit --name rabbit -p 5672:5672 -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3.7.8`

## Docker Compose
- Copy `decentsite/local_settings_docker_example.py` to `decentsite/local_settings.py`
- Adjust the settings like disabling Debug, commenting out the empty password validators and configuring production database details
- `docker-compose up`
- If you need to re-build: `docker-compose up --force-recreate --build`
- In another terminal (or if you ran detached `docker-compose up -d`)
- ssh into the decentmark container (will usually be decentmark_decentmark_1, check with docker-compose ps)
- `docker exec -it decentmark_decentmark_1 bash`
- Create a super user
- `python manage.py createsuperuser --settings decentsite.local_settings`
- Optionally generate some sample units
- `python manage.py generateuser --settings decentsite.local_settings -u 10`
- `python manage.py generatedata --settings decentsite.local_settings -un 1 -an 5 -s 100 -y 2018`
- Now you can exit add add your super user to the unitusers model through the django admin panel with full permissions to view the unit

## References
- [django](https://www.djangoproject.com/) the web framework and its examples
- [gitignore.io](https://www.gitignore.io/)
- [django-todo](https://github.com/shacker/django-todo) for its examples
- [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks) for adding css to forms
