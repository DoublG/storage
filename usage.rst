=======
Usage
=======
-----
Console commands
-----
.. click:: storage:create_table
   :prog: create_table

.. click:: storage:start
   :prog: start

-------------
Configuration
-------------
Configuration is loaded via a configuration file supplied
via the *APP_SETTINGS* environment variable.

Mandatory values in the config file.

=========================== =========================================
Configuration name          Description
=========================== =========================================
*[<RootKey]*                Root header used in *--config_root* parameter
*rabbitmq_user*             RabbitMQ user
*rabbitmq_password*         RabbitMQ password
*rabbitmq_host*             RabbitMQ host
*rabbitmq_exchange*         RabbitMQ exchange name
*rabbitmq_routing_key*      RabbitMQ routing key
*database_uri*              SQLAlchemy uri
*transform_method*          path to transform method (.notation)
=========================== =========================================


Systemd
```````
**/etc/systemd/system/storage.service** ::

    [Unit]
    Description=storage service for Smappee
    After=network.target

    [Service]
    Environment="APP_SETTINGS=/var/www/storage/config.ini"
    ExecStart=/var/www/storage/env/bin/main start --config_root Smappee
    Restart=on-failure
    Type=simple
    User=www-storage
    Group=www-storage

    [Install]
    WantedBy=default.target

----------
Deployment
----------
I'm using fabric for the deployment.

**cleanup of the previous setup** ::

    fab -H root@100.100.0.2 cleanup-application

**update / install new application** ::

    fab -H root@100.100.0.2 build-application

**start service** ::

    systemctl start storage.service

**stop service** ::

    systemctl stop storage.service

**reload configuration** ::

    systemctl daemon-reload

