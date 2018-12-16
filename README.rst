=======
Storage
=======
The storage application is responsible for storing rabbitmq messages in a mysql db.

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

------------------------
Documentation generation
------------------------
I've mostly based myself on the following document:
https://daler.github.io/sphinxdoc-test/includeme.html

**make documentation files**::

    make html

**push updated documentation to github**::

    git push origin gh-pages

