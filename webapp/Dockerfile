FROM python:3.6

# Install application requirements
# Create django user, will own the Django app
ADD ./config/requirements.txt /srv/sptool/
RUN pip3 install -r /srv/sptool/requirements.txt

RUN adduser --no-create-home --disabled-login --group --system django \
    && chown -R django:django /srv/sptool \
    && mkdir /srv/static-files \
    && chown -R django:django /srv/static-files

# Add start script
ADD ./config/start.sh /
# Add load script
ADD ./config/load_data.sh /

# Add uWSGI config
ADD ./config/django-uwsgi.ini /etc/uwsgi/django-uwsgi.ini
ADD ./config/django-uwsgi-dev.ini /etc/uwsgi/django-uwsgi-dev.ini

# Add database check script
ADD ./config/database-check.py /srv/config/database-check.py

# Add code
# ADD ./sptool /srv/sptool

USER django

# Execute start script
CMD ["./start.sh"]
