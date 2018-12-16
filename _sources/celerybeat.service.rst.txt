.. _celerybeat.service:

==================
celerybeat.service
==================
--------------------------------------
/etc/systemd/system/celerybeat.service
--------------------------------------
::

    [Unit]
    Description=Celery Beat Service
    After=network.target

    [Service]
    Type=simple
    User=www-storage
    Group=www-storage
    EnvironmentFile=/var/www/storage/celerybeat
    WorkingDirectory=/var/www/storage
    ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat \
      --pidfile=${CELERYD_PID_FILE} \
      --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

    [Install]
    WantedBy=multi-user.target

