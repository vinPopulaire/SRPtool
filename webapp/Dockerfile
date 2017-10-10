FROM python:3.6

# Add code
ADD ./sptool /srv/sptool

# Install application requirements
# Create django user, will own the Django app
ADD ./config/requirements.txt /srv/sptool/
RUN pip3 install -r /srv/sptool/requirements.txt \
    && adduser --no-create-home --disabled-login --group --system django \
    && chown -R django:django /srv/sptool

# Add start script
ADD ./config/start.sh /

# Add uWSGI config
ADD ./config/django-uwsgi.ini /etc/uwsgi/django-uwsgi.ini

# Add database check script
ADD ./config/database-check.py /srv/config/database-check.py

# Execute start script
CMD ["./start.sh"]
