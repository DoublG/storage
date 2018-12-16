.. _celery:

======
celery
======
-----------------------
/var/www/storage/celery
-----------------------
::

    CELERYD_NODES="w1"
    CELERY_BIN="/var/www/storage/env/bin/celery"
    CELERY_APP="storage.celery.tasks:app"
    CELERYD_MULTI="multi"
    CELERYD_OPTS="--time-limit=300 --concurrency=2"
    CELERYD_PID_FILE="/tmp/%n.pid"
    CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
    CELERYD_LOG_LEVEL="INFO"

    APP_SETTINGS="/var/www/storage/celery.ini"

