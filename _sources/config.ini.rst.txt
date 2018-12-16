.. _config.ini:

==========
config.ini
==========
---------------------------
/var/www/storage/config.ini
---------------------------
::

    [Smappee]
    rabbitmq_user = smappee
    rabbitmq_password = <CHANGEME>
    rabbitmq_host = localhost
    rabbitmq_exchange = amq.topic
    rabbitmq_routing_key = mwsmappee
    database_uri = mysql://<CHANGEME>
    transform_method = storage.format.transform_smappee

