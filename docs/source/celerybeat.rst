.. _celerybeat:

==========
celerybeat
==========
---------------------------
/var/www/storage/celerybeat
---------------------------
::

    CELERY_BIN="/var/www/storage/env/bin/celery"
    CELERYD_PID_FILE="/tmp/beat.pid"
    CELERYD_LOG_FILE="/var/log/celery/beat.log"
    CELERYD_LOG_LEVEL="INFO"
    CELERY_APP="storage.celery.tasks:app"

    APP_SETTINGS="/var/www/storage/celery.ini"

