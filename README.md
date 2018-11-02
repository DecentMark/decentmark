# DecentMark
Automatic grader for programming assignments.

## Running
- `pip install -r requirements.txt`
- `cp decentsite/local_settings_example.py decentsite/local_settings.py`
- `export DJANGO_SETTINGS_MODULE=decentsite.settings`
- `python manage.py migrate`
- `python manage.py runserver`

## Marking
- Install and setup RabbitMQ
- `sudo rabbitmq-server`
- `celery -A decentmark worker -l info` or on windows: `celery -A decentmark worker --pool=eventlet -l info`

## Testing
- Download Selenium driver for your OS and add it to the path environment variable.
- `python manage.py test`

## RabbitMQ for development (alternative to installing RabbitMQ)
- `docker run -d --hostname rabbit --name rabbit -p 5672:5672 -e RABBITMQ_DEFAULT_USER=admin -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3.7.8`

## Docker
- `git clone https://github.com/DecentMark/decentmark.git`
- `cp decentsite/local_settings_docker_example.py decentsite/local_settings.py`
- Adjust the settings like disabling Debug, commenting out the empty password validators and configuring production database details
- `docker-compose up` or if you need to re-build: `docker-compose up --force-recreate --build` add `-d` if you want to run it in the background
- Open another terminal (or if you ran detached `docker-compose up -d` just continue using the current one)
- SSH into the container `docker exec -it decentmark_decentmark_1 bash` (will usually be `decentmark_decentmark_1`, check with `docker-compose ps` if this doesn't work)
- `python manage.py generateuser -u 10`
- `python manage.py generatedata -un 1 -an 5 -s 100 -y 2018`
- `python manage.py createsuperuser`
- Now you can exit add add your super user to the unitusers model through the django admin panel with full permissions to view the created unit
- The server should be accessible from http://localhost and the admin panel at http://localhost/admin
- If using docker toolbox, run `docker-machine ip`. Use that instead of localhost.

## References
- [django](https://www.djangoproject.com/) the web framework and its examples
- [gitignore.io](https://www.gitignore.io/)
- [django-todo](https://github.com/shacker/django-todo) for its examples
- [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks) for adding css to forms
