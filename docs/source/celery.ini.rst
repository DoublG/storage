.. _celery.ini:

==========
celery.ini
==========
----------------------------
 /var/www/storage/celery.ini
----------------------------
::

    [Celery]
    result_backend = db+mysql://<CHANGEME>
    broker_url = amqp://<CHANGEME>
    database_uri = mysql://<CHANGEME>

